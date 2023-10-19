##
from typing import Tuple, Dict

import pandas as pd
from langchain.chat_models import ChatOpenAI
from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from langchain.prompts import ChatPromptTemplate


class RealEstateTextProcessor:
    template_string = """  
        Step:  
        1. translation: The following text is a description of a real estate property: ```{text}```. 
        Translate this text to English.  
        2. features: Look at this text: ```{text}```. From the following text extract property features that directly 
        affect rental or purchase price of the property. 
        Return a dictionary, where the key is one of the 5 categories and values are lists of these features.   
        The feature is a keyword that affects the rental or purchase price of the property, 
        focus especially on these categories:  
        - area_neighborhood (city centre, quiet neighborhood, greenery, parks, rural area, suburb),   
        - amenities (e.g. schools, shops, restaurants, proximity to public transport etc.),   
        - condition (renovated, new, luxurious, before reconstruction, year built, year renovated etc.)  
        - materials_style (parquet, modern, large, bright etc.)  
        - perks_other (beautiful view, parking etc.)  
        Write AS MANY THINGS AS POSSIBLE that have an impact on the price or rent and quality of life in the apartment. 
        If there is no data for that given category, leave the list empty. 
        If you don't know where to categorize something, categorize it in perks_other.  
        The text is: ```{text}```  

        This is an example of features dictionary:               
        ```dict(  
            'area_neighborhood'=['rural', 'lake'],  
            'amenities'=['university', 'restaurant'],  
            'condition'=['year built 1980', 'before reconstruction'],  
            'materials_style'=['parquet'],   
            'perks_other'=['garden'],  
        )```

        {format_instructions}  
        """

    model_name = 'gpt-3.5-turbo'

    @staticmethod
    def _get_output_parser_and_format_instructions() -> Tuple[StructuredOutputParser, str]:
        translation_schema = ResponseSchema(
            name="translation",
            description="Translate the property description text to English.",
        )
        features_schema = ResponseSchema(
            name="features",
            description="Extract property features that directly affect rental or purchase price of the property.",
        )
        response_schemas = [translation_schema, features_schema]
        output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
        format_instructions = output_parser.get_format_instructions()
        return output_parser, format_instructions

    def _get_api_response(self, text: str) -> Dict:
        chat = ChatOpenAI(temperature=0.0, model_name=self.model_name)
        prompt_template = ChatPromptTemplate.from_template(self.template_string)
        output_parser, format_instructions = self._get_output_parser_and_format_instructions()

        prompt = prompt_template.format_messages(
            text=text,
            format_instructions=format_instructions,
        )

        response = chat(prompt)
        output_dict = output_parser.parse(response.content)
        return output_dict

    def process_data(self, df: pd.DataFrame, col_name: str) -> pd.DataFrame:
        translations = []
        features = []

        for index, row in df.iterrows():
            text = row[col_name]
            output_dict = self._get_api_response(text=text)
            translation = output_dict.get("translation", "")
            feature = output_dict.get("features", {})

            translations.append(translation)
            features.append(feature)

        df["text_translated"] = translations
        df["features"] = features

        return df


processor = RealEstateTextProcessor()
result_df = processor.process_data(df=pd.DataFrame(), col_name="text")
