# Flood Solver

Solver for _flood_ game. Code is extracted from the quarto markdown file

```sh
quarto convert flood.qmd --output /dev/stdout --quiet \
  | jupyter nbconvert --to python --stdout --stdin --log-level 50 \
  | sed -e '/^---/,/^---/d' \
  | sed -e '/^#/d' | sponge flood.py

# reformat with black
black flood.py
```

Read article about this project on my [website][1]. Vega-lite Visualization of
results can be found [here][2]


[1]:https://julius383.github.io/posts-output/2024-06-17-using-a*-and-python-to-solve-a-puzzle/
[2]:https://vega.github.io/editor/#/url/vega-lite/N4IgJAzgxgFgpgWwIYgFwhgF0wBwqgegIDc4BzJAOjIEtMYBXAI0poHsDp5kTykBaADZ04JAKyUAVhDYA7EABoQAEzjQATjRyZ289ADUaEBkmEAvJDrkACNgDNrAQQBU1iJiTrrOOOrtt1ZFkoOGsAdzoYayhBBndfAH0oNgZZTGt4Bk13GihKSkUQHUxBODQQF3DI6Nj49SSUtIy4LKMdKELlSxRUUGJTBjU0AG1QZRo7O1yGQUwAT3K4JAgFpXmfRYAPHyhMOGVC-tiy1AAmAGYlGllVTbQABgBfBTGJqagZ+cXl1aK5jfQSF2JkEhwGJ1OAEYrjc4HdUE8Xio3tNZgt0EsVoV1icQHCdnsDkojoM0KcxDDbmhIc9XpNUV8MT9sf9cUDMCCwccydCQNcqagaUjxvSPmjvli1qytgT9lzSWdLnzYfDTrTkaLPui8cypQCQOzOcTwWSACyUuFk9Ui95aiW-HEyuC7OXG7lnADsFvh52tKLFjJ1kr++sNpnlEIAHN60L7hf67Uzg46MdtnYSI2aY6hTX7NeKkw7pYDgeG3QrTqds7n4-nAwh9jQGAgWfr8enXSASRDefzLQi87aCyAG+Nm622aXQeWIVXlQLEXSh-XG+O9bj2y6iV2TWdeyrqYOGdrR02W+vymHpzv3Rds0Kl8fyqe1yGN2mt5mznO+6qjwGT1Xc830vKcv1OL1537NVa2XQCx2AlM8Q-DMZ2paMoJ9f9ExHICJ1AjkyxvBVIQw39Y2w4cX0Q4tkNlbdux5atKJXBD8JLQjr0YxVmNgp90BgTxtyQzdUOIk5SOzRcNTg8pBPUYTaKvcClXIgc+IAuShPYuiOwY3dJMww8NJw+TFNDMC0J4ozBRY7UzJ00TO24wy1Jgx9NIE7SLw4o1xLJCkbPcmT+IwbyQNTeiv0hABObM4w80zwqQ5SrNOAA2eK7K0hTHJQ5yDLimya0S4cHJ8g1LP8s5ArU3MAF1nhHTwAGtyiYTxCjgYI2HGWQyDQUB4VAKY4EEA50HIpr0RGmgxom-yKoARxMNI6EsGhSBAJrNgAeUmCA4EwQaQFG8bykdJrkliBA9Fm+byhtJ8rrYQQAhOs6Fsux5HiAA/view
