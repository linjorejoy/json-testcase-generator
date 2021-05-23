## JSON Test Case Generator

You can use the [JSON Test Case Generator](https://github.com/linjorejoy/json-testcase-generator) to generate many JSON files in a controlled manner

- [JSON Test Case Generator](#json-test-case-generator)
- [Features](#features)
- [How to Use](#how-to-use)
  - [Initializing the JSON File](#initializing-the-json-file)
  - [Start Page](#start-page)
  - [Uploading the JSON File](#uploading-the-json-file)
  - [Process Variables](#process-variables)
    - [Generating All Permutations](#generating-all-permutations)
    - [Generating Using Table](#generating-using-table)
  - [Naming the Files](#naming-the-files)
  - [Preview](#preview)
  - [Generate](#generate)
- [Jekyll Themes](#jekyll-themes)
- [Support or Contact](#support-or-contact)

---

## Features

- Supports 4 Data Types and null value

  - `string`
  - `int`
  - `float`
  - `bool`
  - `null`

- Template based, So you can use the same template for several test cases

---

## How to Use

### Initializing the JSON File

To initialize all the variablesto the Application, the JSON File needs to be prepped.

You can initialize the variables by remapping then in the pattern `$variableName$`. For Example,

![JSON Example](resources/other_images/jsonexample2.svg)

In the above example there are 6 variables initialized which are marked in bright green.

> Note : For all Data Types(`string`, `int`, `float`, `bool` or `null`), enclose the mapped variables inside double quotes as shown in the above example.

You can also concatenate variables together or with other strings as shown in the below example.

![Image](resources/other_images/jsonexample5.svg)

---

### Start Page

You can select 2 paths from here.

- [Generate All Permutation](#generating-all-permutations)
- [Generate Using Table](#generating-using-table)

![StartPage](resources/other_images/startpage2.jpg)

---

### Uploading the JSON File

Click on the **Select File** Button and select the JSON template file that you created in your [previous step](#initializing-the-json-file).

Upload Page snapshot :

![UploadPage](resources/other_images/uploadpage3.jpg)

---

### Process Variables

This is the step where you have to define the test cases that needs to be created.

#### Generating All Permutations

It will generate all the Permutations of the variation of all the inputs provided.

For Example, assume there are `4` variables having `8, 8, 7, 8` variations respectively. Then it will create.

> 8 x 8 x 7 x 8 = 3584 different variations

**So the number of variations can increase very fast.**

![Image](resources/nn4.svg)

> As Stan Lee (May he Rest in Peace) in his Spider Man Comics once Said [**With great power comes great responsibility**](https://en.wikipedia.org/wiki/With_great_power_comes_great_responsibility), you should use this method cautiously.

#### Generating Using Table

Markdown is a lightweight and easy-to-use syntax for styling your writing. It includes conventions for

---

### Naming the Files

Markdown is a lightweight and easy-to-use syntax for styling your writing. It includes conventions for

---

### Preview

Markdown is a lightweight and easy-to-use syntax for styling your writing. It includes conventions for

---

### Generate

Markdown is a lightweight and easy-to-use syntax for styling your writing. It includes conventions for

```markdown
Syntax highlighted code block

# Header 1

## Header 2

### Header 3

- Bulleted
- List

1. Numbered
2. List

**Bold** and _Italic_ and `Code` text

[Link](url) and ![Image](src)
```

For more details see [GitHub Flavored Markdown](https://guides.github.com/features/mastering-markdown/).

## Jekyll Themes

Your Pages site will use the layout and styles from the Jekyll theme you have selected in your [repository settings](https://github.com/linjorejoy/json-testcase-generator/settings/pages). The name of this theme is saved in the Jekyll `_config.yml` configuration file.

## Support or Contact

Having trouble with Pages? Check out our [documentation](https://docs.github.com/categories/github-pages-basics/) or [contact support](https://support.github.com/contact) and we’ll help you sort it out.
