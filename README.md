# Markov Chain Model for Understanding Customer Decisions

Regardless of what company you work at, chances are you'll encounter an orders table that looks like this:

| order_id | customer_id | order_num | order_date          | item                    |
| -------- | ----------- | --------- | ------------------- | ----------------------- |
| 1931     | 1           | 0         | 2020-11-24 10:54:19 | Haunted Mansion         |
| 4040     | 2           | 0         | 2020-11-24 11:31:51 | Indiana Jones Adventure |
| 6444     | 2           | 1         | 2020-11-24 12:40:51 | Space Mountain          |

If so, you're in luck. This project can help you get started with the following goals:

1. Understand customer decisions through the Markov chain model
2. Use the Markov chain model to simulate customer orders data
3. Visualize customer decisions using an out-of-the-box Sankey diagram

For more information, please read my [blog post](https://harrisonized.github.io/2020/12/03/customer-history-markov.html).



## Getting Started

Please build the following conda environment:

```bash
conda create --name markov_env python=3.7
conda activate markov_env
conda install conda
conda install jupyter

conda install numpy
conda install pandas
conda install -c conda-forge webcolors
conda install -c plotly plotly==4.5.0
conda install -c conda-forge pydotplus
pip install simpy
pip install pygraphviz
```



## License

This project is licensed under the terms of the [MIT license](https://github.com/harrisonized/customer-history-markov/blob/master/LICENSE). If you choose to use this as a building block for your own project, please fork this repository, clone from your own fork, and give me due credit in a CREDITS.md file ([example](https://github.com/harrisonized/harrisonized.github.io/blob/master/CREDITS.md)).