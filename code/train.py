import mlflow
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_score, recall_score, f1_score
from download_dataset import aquire_training_data

def main():
        X, y = aquire_training_data()
        x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=43, stratify=y)

        clf = RandomForestClassifier(bootstrap=True, 
                                     criterion='gini', 
                                     min_samples_split=2, 
                                     min_weight_fraction_leaf=0.0, 
                                     n_estimators=50, 
                                     random_state=34, 
                                     verbose=0)
        mlflow.set_tracking_uri("http://localhost:5000")
        # Check if the experiment exists
        expr = mlflow.get_experiment_by_name('experiment_1')
        if expr is None:
            # Create the experiment if it doesn't exist
            expr = mlflow.create_experiment('experiment_1')

        # Set the experiment
        mlflow.set_experiment(expr.experiment_id)
        with mlflow.start_run():
            clf.fit(x_train, y_train)
            predicted = clf.predict(x_test)

            mlflow.sklearn.log_model(clf, "model_random_forest")
            mlflow.log_metric("precision_label", precision_score(y_test, predicted, average='weighted'))
            mlflow.log_metric("f1_score_label", f1_score(y_test, predicted, average='weighted'))
            mlflow.log_metric("recall_label", recall_score(y_test, predicted, average='weighted'))
        
if __name__ == "__main__":
    main()
