set -x
download_code () {
    local OUTPUT=$1
    OUTPUT=`sed -e 's/,$//' -e 's/^"//'  -e 's/"$//g'  <<<"$OUTPUT"`
    url=$(aws lambda get-function --function-name $1 --query 'Code.Location' |jq '.' -r)
    wget $url -O $OUTPUT.zip
}

FUNCTION_LIST=$(aws lambda list-functions --query Functions[*].FunctionName | jq '.[]' -r)
for run in $FUNCTION_LIST
do
    download_code $run
done
