# wbm_ai_kg
Google Summer of Code (GSoC) 2024 Wayback Machine GenAI Knowledge Graph project

# Wayback Machine CDX Fetcher

This Python script fetches data from the Wayback Machine CDX API for a given URL, filters the data, and saves it to a TSV (Tab-Separated Values) file. It also downloads and saves the archived content for each filtered record.

## Requirements

- Python 3.6+
- `requests`
- `pandas`
- `tqdm`
- `argparse`
- `os`

You can install the required Python libraries using the following command:
```
pip install requests pandas tqdm
```

## Usage

### Command Line Arguments

- `url`: The URL to search in the Wayback Machine.
- `output`: The output TSV file name.
- `--full`: Optional flag to dump full data without filtering.
- `--num_lines`: Optional parameter to specify the number of lines to save from the end of the TSV. Default is 10.

### Example Command

```bash
python wayback_fetcher.py <url> <output> [--full] [--num_lines <num>]
```

### Example Usage

```bash
python wayback_fetcher.py example.com output.tsv --num_lines 5
```

This command will fetch the CDX data for `example.com`, filter it, save the last 5 lines to `output.tsv`, and download the corresponding archived content.

## Code Explanation

### `fetch_cdx_data(url)`

This function fetches data from the Wayback Machine CDX API for the given URL and returns a pandas DataFrame. It uses the `requests` library to make the API request.

### `filter_data(df)`

This function filters the DataFrame to include only rows where the `mimetype` is `text/html` and the `statuscode` is `200`. It returns a DataFrame with only the `timestamp` and `original` columns.

### `save_to_tsv(df, filename, num_lines=10)`

This function saves the last `num_lines` of the DataFrame to a TSV file. It uses a progress bar to indicate the saving process.

### `fetch_and_save_content(row, base_dir)`

This function fetches the archived content for a given row and saves it to a file. It creates a directory named after the `timestamp` inside the `base_dir` and saves the content as `content.html`.

### `main`

The main function parses command-line arguments, fetches the CDX data, optionally filters it, saves the data to a TSV file, and fetches the content for each filtered record.

## Notes

- Ensure that the provided URL is properly formatted.
- The script creates directories and files in the current working directory.
