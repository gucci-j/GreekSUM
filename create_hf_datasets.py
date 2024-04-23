

import json
import os
import pandas as pd


def restructure_data(data: dict, file_name: str) -> dict:
    return {
        "id": file_name.split('.json')[0],
        "url": data['url'],
        "title": data['title'],
        "summary": data["abstract"],
        "text": data["article"],
    }


def main(args):
    # Load split data .txt info
    with open(args.split_train_data_path, 'r') as f:
        train_name_data = f.read().splitlines() 
    with open(args.split_test_data_path, 'r') as f:
        test_name_data = f.read().splitlines() 
    
    # Load the data
    train_data = []
    test_data = []
    for train_file_name in train_name_data:
        with open(os.path.join(args.data_dir, train_file_name), 'r') as f:
            data = json.load(f)
            data = restructure_data(data, train_file_name)
            train_data.append(data)

    for test_file_name in test_name_data:
        with open(os.path.join(args.data_dir, test_file_name), 'r') as f:
            data = json.load(f)
            data = restructure_data(data, test_file_name)
            test_data.append(data)
    
    # Convert into DataFrame
    train_df = pd.DataFrame(train_data)
    test_df = pd.DataFrame(test_data)

    # Save the data as .csv
    train_df.to_csv(args.train_data_path, index=False)
    test_df.to_csv(args.test_data_path, index=False)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Create HF datasets')
    parser.add_argument('--data_dir', type=str, default='data', help='Path to the data directory')
    parser.add_argument('--split_train_data_path', type=str, default='data/train.txt', help='Path to the split train data')
    parser.add_argument('--split_test_data_path', type=str, default='data/test.txt', help='Path to the split test data')
    parser.add_argument('--train_data_path', type=str, default='data/train.csv', help='Path to save the train data')
    parser.add_argument('--test_data_path', type=str, default='data/test.csv', help='Path to save the test data')
    parser.add_argument(
        "--repo_name",
        type=str,
        help="The name of the repository to which the data will be uploaded",
    )
    parser.add_argument(
        "--repo_dir",
        type=str,
        help="The path to the repository directory",
    )
    args = parser.parse_args()
    main(args)


    from huggingface_hub import HfApi
    api = HfApi()
    api.upload_folder(
        folder_path=args.repo_dir,
        repo_id=args.repo_name,
        repo_type='dataset',
    )