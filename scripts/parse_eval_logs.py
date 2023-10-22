import os
import re
import csv
import pathlib
import sys

def get_files(directory: str) -> list[str]:
    contents = os.listdir(directory)
    files = [f for f in contents if os.path.isfile(directory+'/'+f)] #Filtering only the files.
    return files

def get_accuracy_metric(filename: str) -> str:
    file = open(filename, 'r')
    metric = None

    reg = re.compile("accuracy: (\d+\.\d+)")
    for line in file:
        res = reg.search(line)
        if res:
            metric = res.group(1)
            break
    
    return metric

def get_num_of_samples(filename: str) -> str:
    file = open(filename, 'r')
    saples = None

    reg = re.compile("Evaluating (\d+) samples")
    for line in file:
        res = reg.search(line)
        if res:
            samples = res.group(1)
            break
    
    return samples


if __name__ == '__main__':
    model = sys.argv[1]
    base_path = sys.argv[2] #"/student/abeiler/evaluation_data/logs/"
    out_dir = sys.argv[3]
    files = get_files(base_path+model)

    rows = []
    for file in files:
        filepath = base_path + model + "/" + file
        res = get_accuracy_metric(filepath)
        samples = get_num_of_samples(filepath)
        rows.append([model, pathlib.Path(file).stem, res, samples])

    filename = out_dir + model + "_eval_results.csv"
    
    fields = ['Model', 'Eval', 'Accuracy', 'NumOfSamples']
    # writing to csv file  
    with open(filename, 'w') as csvfile:  
        # creating a csv writer object  
        csvwriter = csv.writer(csvfile)  

        # writing the fields  
        csvwriter.writerow(fields)  
                                            
        # writing the data rows  
        csvwriter.writerows(rows)
