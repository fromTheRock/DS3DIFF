from S3Ops import S3Ops as s3

def main() -> None:
    """Main entry point of the script"""
    endpoint, region = s3.getConnectionData()
    client = s3.getS3Client(endpoint)
    response = s3.listBuckets(client, endpoint, region)
    #print(response)
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        print('S3 buckets listed successfully.')
    else:
        print(f'Error: {response["ResponseMetadata"]["HTTPStatusCode"]}')
        return
    
    bucket_list = s3.printBucketNames(response)
    if bucket_list:
        selected_num = s3.getValidBucketNumber(len(bucket_list))
        selected_bucket = bucket_list[selected_num - 1]['Name']
        print(f"You selected bucket: {selected_bucket}")
        
        #TODO: selected_bucket must be in the format Bucket-name.s3express-zone-id.region-code.amazonaws.com
        #print(s3.bucketList(client, response, selected_bucket))
    else:
        print("No buckets found")

if __name__ == "__main__":
    main()
