## Compressed Row-Access Matrix file format.

Goal : Simple and Efficient storage of 2d sparse matrices for memory efficient access of rows columns and ranges.

## File Structure:
1. Header Section:
    - Describes the overall file metadata.
    - Fixed size for simplicity.

2. Index Section:
    - Row Index
        - Maps rows to their corresponding data offsets in the file.
    <!-- - Column Index
        - Maps columns to their corresponding data offsets in the file. -->

3. Data Section:
    - Row Data
        - Contains the actual sparse matrix data in a compressed Row Format. along with the column number
    <!-- - Column Data
        - Contains the actual sparse matrix in compressed Column Format. -->


## Detailed Layout

### 1. Header Section

Description: File identifiers and general fine info  
Size: 40 bytes

| Field | Type | Size (Bytes) | Description |
|-------|------|--------------|-------------|
| Magic Number | ASCII | 4 | File identifier - CRAM |
| Version | Integer | 2 | File format version |
| Rows | Integer | 4 | Number of rows in the matrix |
| Columns | Integer | 4 | Number of columns in the matrix |
| Non-Zero Count | Integer | 8 | Total number of non-zero entries |
| Index Offset | Integer | 8 | Byte offset to the index section |
| Data Offset | Integer | 8 | Byte offset to the data section |


### 2. Index Section

Description: Maps Rows to their corresponding data offsets  
Size: 16 bytes

| Field | Type | Size (Bytes) | Description |
|-------|------|--------------|-------------|
| Row ID | Integer | 4 | Row ID |
| Offset | Integer | 8 | Byte offset in the data section |
| Non-Zero Count | Integer | 4 | Number of non-zero entries |


### 3. Data Section

Description: Data elements of the  
Size: 8

| Field | Type | Size (Bytes) | Description |
|-------|------|--------------|-------------|
| Column Index | Integer | 4 | Column index of the value |
| Value | Float | 4 | The matrix value |



