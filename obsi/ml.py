import pandas as pd
from sklearn.base import TransformerMixin
from sklearn.decomposition import NMF
from sklearn.pipeline import FeatureUnion, Pipeline
from sklearn.tree import DecisionTreeClassifier


class NoteToTagTransformer(TransformerMixin):
    def __init__(self, except_tag):
        self.except_tag = except_tag

    def fit(self, X, y=None):
        self.tags = {tag for note in X for tag in note.tags if tag != self.except_tag}
        return self

    def transform(self, X, y=None):
        df = pd.DataFrame(X, columns=["note"])
        for tag in self.tags:
            df[tag] = df["note"].apply(lambda n: tag in n.tags)
        return pd.DataFrame(df[self.tags], columns=self.tags).fillna(False)

    def get_feature_names(self):
        return self.tags


class NMFDataFrame:
    def __init__(self, *args, **kwargs):
        self.nmf = NMF(*args, **kwargs)

    def fit(self, X, y):
        self.nmf.fit(X, y)
        return self

    def transform(self, X, y=None):
        return pd.DataFrame(
            self.nmf.transform(X),
            columns=[f"nmf_{i}" for i in range(self.nmf.n_components_)],
        )


class FeatureUnionDataFrame(TransformerMixin):
    def __init__(self, *args, **kwargs):
        self.fu = FeatureUnion(*args, **kwargs)

    def fit(self, X, y=None, **kwargs):
        self.fu.fit(X, y, **kwargs)
        return self

    def transform(self, X, y=None, **fit_params):
        return pd.DataFrame(self.fu.transform(X), columns=self.fu.get_feature_names())

    def get_feature_names(self):
        return self.fu.get_feature_names()

    def set_params(self, **kwargs):
        self.fu.set_params(**kwargs)

    def get_params(self, deep=False):
        return self.fu.get_params(deep)


class NotePathTransformer(TransformerMixin):
    def fit(self, X, y=None):
        self.paths = set()
        for note in X:
            self.paths.add(note.path.parent)
        return self

    def transform(self, X, y=None):
        df = pd.DataFrame()
        for path in self.paths:
            df[str(path)] = [x.path.is_relative_to(path) for x in X]
        return df

    def get_feature_names(self):
        return [str(p) for p in self.paths]


def generate_tag_recommendations(notes, probability_min=0.33):
    """
    Geneate suggestions for tags.
    :param notes: notes used for training
    :return: (tag, notes)
    """
    assert isinstance(notes, list)

    tags = {tag for note in notes for tag in note.tags}
    for tag in tags:
        pipeline = Pipeline(
            steps=[
                # attributes per note:
                (
                    "fu",
                    FeatureUnionDataFrame(
                        [
                            # tags
                            ("tags", NoteToTagTransformer(except_tag=tag)),
                            # parent folders
                            ("paths", NotePathTransformer()),
                            # todo incoming links
                            # todo outgoing links
                            # todo words
                        ]
                    ),
                ),
                ("fa", NMFDataFrame(init="nndsvda")),
                ("clf", DecisionTreeClassifier(min_samples_leaf=5)),
                # ("clf", KNeighborsClassifier(n_neighbors=3)),
            ]
        )

        # train
        df_train = pd.DataFrame(notes, columns=["note"])
        df_train["y"] = [tag in n.tags for n in notes]
        in_count = len(df_train[~df_train["y"]])
        if in_count > 10:
            pipeline.fit(df_train["note"].values, df_train["y"])

            # predict
            df_predict = pd.DataFrame(df_train[~df_train["y"]])
            prediction_proba = pipeline.predict_proba(df_predict["note"].values)
            df_res = pd.DataFrame(prediction_proba, columns=["out", "in"])
            df_res["note"] = df_predict["note"].values

            notes_in = (
                df_res[df_res["in"] > probability_min]
                .sort_values("in", ascending=False)["note"]
                .values
            )
            yield tag, notes_in
