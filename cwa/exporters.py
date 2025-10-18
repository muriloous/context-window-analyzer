import time, os, random
import pandas as pd
from pandas import DataFrame
import scipy.cluster.hierarchy as hac
import matplotlib.pyplot as plt

from processing import ContingencyTable
from metrics import (
    vectorize_contingency_table,
    get_linkage_matrix,
    ComparativeTable
)

def make_dataframe_from_contingency_dict(contingency_table: ContingencyTable) -> DataFrame:
    df = pd.DataFrame(data=contingency_table.data,
                      index=contingency_table.header)
    return df.T

def export_contingency_table_to_csv(contingency_table: ContingencyTable, filename: str = 'corpus') -> str:
    '''
    Use pandas to export contingency table as csv

    '''
    path = os.getcwd() + '/exports/contingency_tables'
    
    partial_alias = os.path.splitext(filename)[0]
    alias = f'{partial_alias or 'corpus'}_contingency_table'
    timestamp = f'{int(time.time())}_{random.randint(1000,9999)}'
    output_file = f'{path}/{timestamp}_{alias}.csv'

    df = make_dataframe_from_contingency_dict(contingency_table.data)
    df.to_csv(output_file, encoding='utf-8')

    return output_file

def export_comparative_table(comparative_table: ComparativeTable) -> str:
    output = os.getcwd() + '/exports/comparative_tables' + f'/comparative_{int(time.time())}' + '.csv'

    df = pd.DataFrame(
        data=comparative_table.data,
        index=comparative_table.index)
    
    df.to_csv(output, encoding='utf-8')

    return output

def make_dendrogram(contingency_table: ContingencyTable, title: str = "Dendrogram from Spearman correlation") -> tuple[list[list[float]], list[str]]:
    matrix = vectorize_contingency_table(contingency_table)

    linkage_matrix = get_linkage_matrix(matrix)
    
    hac.dendrogram(linkage_matrix, labels=contingency_table.target_words, leaf_rotation=45)
    plt.title(title)
    plt.xlabel("Words")
    plt.ylabel("Distance")
    plt.show()

    return linkage_matrix
