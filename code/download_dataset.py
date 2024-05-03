from sklearn.datasets import load_iris


def aquire_training_data():
    return load_iris(return_X_y=True, as_frame=True)
