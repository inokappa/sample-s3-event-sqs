#!/bin/bash
#
. ./_function.sh

# メッセージの取得
function get_sqs_message() {
  aws sqs receive-message --queue-url ${QUEUE_URL} > MESSAGE
}

# メッセージを削除
function delete_sqs_message() {
  aws sqs delete-message --queue-url ${QUEUE_URL} --receipt-handle ${1}
}

# オブジェクトの取得
function get_object_from_s3() {
  echo "aws s3 cp s3://${1}/${2} ./images/"
  aws s3 cp s3://${1}/${2} ./images/
}

# 後処理
function teardown() {
  # オブジェクトの取得が成功したら ReceiptHandle を利用してメッセージを削除
  delete_sqs_message ${1}
  # ダウンロード済みのメッセージを削除
  rm MESSAGE
}
#
# Main
#
while :
do
  get_sqs_message
  
  if [ -s MESSAGE ];then
    cat MESSAGE
    # バケット名の取得
    BUCKET_NAME=`cat MESSAGE | jq -r '.Messages[].Body' | jq -r '.Records[].s3.bucket.name'`
    # オブジェクト名の取得
    OBJECT_KEY_NAME=`cat MESSAGE | jq -r '.Messages[].Body' | jq -r '.Records[].s3.object.key'`
    # ReceiptHandle の取得
    SQS_RECEIPT_HANDLE=`cat MESSAGE | jq -r '.Messages[].ReceiptHandle'`
  
    # 複数オブジェクトが同時にアップロードされた際にスラッシュで終わるオブジェクト名がメッセージに含まれるので...
    if [[ ! ${OBJECT_KEY_NAME} =~ .*/$ ]];then
      # オブジェクトの取得
      get_object_from_s3 ${BUCKET_NAME} ${OBJECT_KEY_NAME}
      if [ $? = "0" ];then
        teardown ${SQS_RECEIPT_HANDLE}
      fi
    else
      teardown ${SQS_RECEIPT_HANDLE}
    fi
  else
    echo "Message not received."
    rm MESSAGE
  fi

  sleep 60
done
