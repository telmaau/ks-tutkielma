## 1. Preprocessing

- construct_graphs.ipynb contains the code to query the relevant information from the Booksampo semantic web. Two subgraphs are created, one for Finnish and one for translated novels. I paid attention particularly to the annotations of nationalities and languages and corrected them to remove some artifacts in the analysis.

- theme_graphs.ipynb is a similar script to query all theme and genre annotations for the novels.

- graphs2csv.ipynb contains the code with which I created dataframes from the knowledge graphs saved in the previous steps.

- other notebooks are for checking the results and correcting some details.