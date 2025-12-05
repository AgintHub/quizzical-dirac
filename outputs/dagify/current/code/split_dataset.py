# -- PRD --
# 1. BULLET: Load the feature matrix CSV from the parent node (assemble_feature_matrix).
#   Reason: The parent node provides the complete feature matrix that needs to be split
#           into training, validation, and test sets. This is the input for
#           this node's processing.
#   Impact: HIGH
#   Complexity: LOW
#   Method: Use a CSV parsing library to load the `feature_matrix_csv` output from the
#           `assemble_feature_matrix` node. Handle potential file reading
#           errors.
# 
# -----------------------------------------------------------------------------
# 2. BULLET: Convert the loaded CSV data into a Pandas DataFrame.
#   Reason: Pandas DataFrames provide an efficient and easy-to-use structure for
#           manipulating and splitting tabular data.
#   Impact: HIGH
#   Complexity: LOW
#   Method: Use the `pd.read_csv()` function in Pandas to convert the CSV string to a
#           DataFrame. Ensure the 'Date' column is correctly parsed as a
#           datetime object.
# 
# -----------------------------------------------------------------------------
# 3. BULLET: Calculate the indices for splitting the DataFrame based on the specified
#   proportions (60% training, 20% validation, 20% testing).
#   Reason: The problem requires a specific time-based split, so we need to determine
#           the row indices that correspond to these percentages of the
#           total dataset length.
#   Impact: HIGH
#   Complexity: MEDIUM
#   Method: 1. Get the total number of rows in the DataFrame using `len(df)`. 2.
#           Calculate training set size: `train_size = int(len(df) * 0.6)`.
#           3. Calculate validation set size `validation_size = int(len(df)
#           * 0.2)`. These sizes are used to slice the dataframe. Round
#           down to integer values to avoid indexing errors. Also note that
#           `test_size` is implicitly `len(df) - train_size -
#           validation_size`.
# 
# -----------------------------------------------------------------------------
# 4. BULLET: Split the DataFrame into training, validation, and test sets using the
#   calculated indices.
#   Reason: This creates the subsets of the data that will be used for model training,
#           validation, and testing, fulfilling the primary objective of
#           the node.
#   Impact: HIGH
#   Complexity: LOW
#   Method: Use DataFrame slicing to create the three datasets: `train_df =
#           df[:train_size]`, `validation_df = df[train_size:train_size +
#           validation_size]`, and `test_df = df[train_size +
#           validation_size:]`. Ensure that there are no overlaps between
#           slices.
# 
# -----------------------------------------------------------------------------
# 5. BULLET: Convert each DataFrame subset back into a CSV-formatted string.
#   Reason: The output structure requires the split datasets to be in CSV format.
#   Impact: HIGH
#   Complexity: LOW
#   Method: Use the `df.to_csv()` function in Pandas for each of the three DataFrames
#           (`train_df`, `validation_df`, `test_df`). Ensure `index=False`
#           to avoid including the DataFrame index as a column in the CSV.
# 
# -----------------------------------------------------------------------------
# 6. BULLET: Store the CSV strings into the respective output variables: `train_csv`,
#   `validation_csv`, and `test_csv`.
#   Reason: This prepares the output data in the format expected by downstream nodes.
#   Impact: HIGH
#   Complexity: LOW
#   Method: Assign the output of `df.to_csv()` for each DataFrame to the corresponding
#           output variable (train_csv, validation_csv, test_csv).
# 
# -----------------------------------------------------------------------------
# 7. BULLET: Implement error handling throughout the process.
#   Reason: To gracefully handle potential issues such as incorrect data formats,
#           missing dependencies, and to provide informative error
#           messages, robust error handling must be implemented.
#   Impact: HIGH
#   Complexity: MEDIUM
#   Method: Use `try...except` blocks to catch potential exceptions during CSV parsing,
#           DataFrame manipulation, and file operations. Log errors and
#           provide meaningful feedback. Handle edge cases where the input
#           CSV might be empty or have missing values.
# -- END PRD --

from pydantic import BaseModel, Field


class AssembleFeatureMatrixOutput(BaseModel):
    """Pydantic model for assemble_feature_matrix node outputs."""
    feature_matrix_csv: str = Field(..., description="CSV\u2011formatted string containing the complete feature matrix with a Date column, all merged feature columns, and a Target column for the next\u2011day return.")


class SplitDatasetOutput(BaseModel):
    """Pydantic model for split_dataset node outputs."""
    train_csv: str = Field(..., description="CSV formatted text containing the training subset of the feature matrix.")
    validation_csv: str = Field(..., description="CSV formatted text containing the validation subset of the feature matrix.")
    test_csv: str = Field(..., description="CSV formatted text containing the test subset of the feature matrix.")


def split_dataset(assemble_feature_matrix_input: AssembleFeatureMatrixOutput, **kwargs) -> SplitDatasetOutput:
    """Partition the feature matrix into training, validation, and test sets using a time‑based split.

    Args:
        assemble_feature_matrix_input: Input from the 'assemble_feature_matrix' node.
        **kwargs: Additional keyword arguments.

    Returns:
        SplitDatasetOutput: Object containing outputs for this node.
    """
    # TODO: Implement this function

    # Return stub output with placeholder values
    return SplitDatasetOutput(
        train_csv="",
        validation_csv="",
        test_csv="",
    )