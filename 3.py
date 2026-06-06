# import ast
# import pandas as pd

# meta_data["belongs_to_collection"] = meta_data["belongs_to_collection"].apply(
#     lambda x: ast.literal_eval(x).get("name", "No Collection")
#     if pd.notna(x) and str(x).startswith("{")
#     else "No Collection"
# )


# import ast

# meta_data["genres"] = meta_data["genres"].apply(
#     lambda x: [i["name"] for i in ast.literal_eval(x)]
# )
# meta_data["genres"] = meta_data["genres"].apply(lambda x: " ".join(x))


# import ast

# meta_data["production_companies"] = meta_data["production_companies"].fillna("[]")

# meta_data["production_companies"] = meta_data["production_companies"].apply(
#     lambda x: " ".join(
#         [i["name"] for i in ast.literal_eval(x)]
#     )
# )
