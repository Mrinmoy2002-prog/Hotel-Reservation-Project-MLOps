from scipy.stats import randint, uniform

LIGHTGM_PARAMS = {
    "n_estimators": randint(100, 200),
    "max_depth": randint(3, 30),
    "learning_rate": uniform(0.01, 0.3),
    "num_leaves": randint(20, 80),
    "boosting_type": ["gbdt", "dart","goss"]
}

RANDOM_SEARCH_PARAMS = {
    "n_iter": 50,   
    "scoring": "accuracy",
    "cv": 5,
    "verbose": 2,
    "random_state": 42,
    "n_jobs": -1
}