# Databases II Final Project

This project has obtained from the Open Data Portal of the Brazilian Federal Government a CSV dataset which contains information on a series of air accidents and incidents occurred within the Brazilian territory and reported to the Brazilian aeronautical authorities &mdash; that is, the National Civil Aviation Agency (ANAC) and the Brazilian Air Force (FAB). The original dataset (file `datasets/V_OCORRENCIA_AMPLA.csv`) is available [here](https://dados.gov.br/dados/conjuntos-dados/ocorrncias-aeronuticas), and its data dictionary, as well as its official description, can be accessed on ANAC's official website through [this link](https://www.anac.gov.br/acesso-a-informacao/dados-abertos/areas-de-atuacao/seguranca-operacional/ocorrencias-aeronauticas/metadados-do-conjunto-de-dados-ocorrencias-aeronauticas).

This project aims at answering the following questions:
1. What strategies can/should be adopted by the regulatory authorities in order to prevent air accidents?
2. It is known that the take off and the landing phases are the most critical. How much do the condition of the airports impact on the success of those operations?

The file `scripts/pre_processing.csv` carries out the pre-processing on the data so that it can be loaded to Microsoft Power BI and the dashboard used for answering the above questions can be built.

The full report in Portuguese is in the `docs/report.pdf` file.
