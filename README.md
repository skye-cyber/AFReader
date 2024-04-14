# AFReader(Animated File Reader)
Animate the didplay of file text content

## Installation

1. Clone the repository:

   ```shell
   git clone https://github.com/skye-cyber/AFReader.git
   ```

2. Navigate to the project directory:

   ```shell
   cd AFReader
   ```

3. Install the required dependencies:

   ```shell
   pip install -r requirements.txt
   ```
4.Install the package:
   ```shell
   pip install ./
   ```


## Usage

To run the CLI app, use the following command:

```shell
AFReader [options] input_file speed
```

Replace `[options]` with the appropriate command-line options based on the functionality you want to execute.

## Available Options

- `1`:`-i/--input_file`  file to read
- `2`:`-s/--speed` text display speed default 0.001

## Examples

1. Example command 1:

   ```shell
   AFReader -i example.txt
   ```
2. Example 2:
```shell
AFReader --input_file example.txt
```
3. Example command 3:

   ```shell

   AFReader -i example.txt -s 0.0001
   ```
3. Example 4:
```shell
   AFReader --input_file example.txt --speed 0.0001
```

## Contributing

Contributions are welcome! If you encounter any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is an open source software.


Feel free to modify and customize this template according to your specific project requirements and add any additional sections or information that you think would be helpful for users.

