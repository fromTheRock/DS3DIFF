'''
Sample module that ask for the bucket to open
and get the list of all object in the bucket chosen.
'''
from src.config import Config
from src.files.s3_ops import S3Ops

def get_valid_bucket_number(max_buckets: int) -> int:
    '''
    Get and validate user input for bucket selection.
    
    Args:
        max_buckets (int): Maximum number of buckets to choose from
        
    Returns:
        int: Validated bucket number
    '''
    while True:
        try:
            value = input('Which bucket do you want to list? (Enter a number): ')
            bucket_num = int(value)
            if 1 <= bucket_num <= max_buckets:
                return bucket_num
            else:
                print(f'Please enter a number between 1 and {max_buckets}')
        except ValueError:
            print('Please enter a valid integer')


def main() -> None:
    '''Main entry point of the script'''

    cfg = Config()
    s3 = S3Ops(cfg)
    if s3.s3_client is None:
        print('Error: S3 client is not initialized')
        return
    response = s3.list_buckets()

    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        print('S3 buckets listed successfully.')
    else:
        print(f'Error: {response["ResponseMetadata"]["HTTPStatusCode"]}')
        return

    bucket_list = s3.print_bucket_names(response)
    if bucket_list:
        selected_num = get_valid_bucket_number(len(bucket_list))
        selected_bucket = bucket_list[selected_num - 1]['Name']
        print(f"You selected bucket: {selected_bucket}")
 
        print(s3.list_files(selected_bucket))
    else:
        print("No buckets found")

if __name__ == "__main__":
    main()

#def main() -> None:
#    '''Main entry point of the script'''
#
#    s3 = S3Ops()
#    response = s3.list_buckets()
#    #print(response)
#    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
#        print('S3 buckets listed successfully.')
#    else:
#        print(f'Error: {response["ResponseMetadata"]["HTTPStatusCode"]}')
#        return
#    
#    bucket_list = s3.print_bucket_names(response)
#    if bucket_list:
#        selected_num = getValidBucketNumber(len(bucket_list))
#        selected_bucket = bucket_list[selected_num - 1]['Name']
#        print(f"You selected bucket: {selected_bucket}")
#        
#        print(s3.list_files(selected_bucket))
#    else:
#        print("No buckets found")
#
#if __name__ == "__main__":
#    main()
#