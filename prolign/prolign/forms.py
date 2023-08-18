import re
import requests

from flask_wtf import FlaskForm
from wtforms import TextAreaField, RadioField, DecimalRangeField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, NumberRange, ValidationError
from protlign.parse_utils import fasta_sequence_parser

# ----------------------------------------------------------------------------------------------------------------------
# Custom Error Messages
# ----------------------------------------------------------------------------------------------------------------------

fasta_format_validation_error = "Invalid FASTA Sequence, Please ensure the presence of caret ('>') in header, " \
                                "validity of Amino Acid one letter codes and absence of special characters or symbols " \
                                "(including new line)"
text_format_validation_error = "Invalid Sequence, ensure validity of Amino Acid one letter codes & " \
                               "absence of special characters or symbols (including new line)."
ncbi_accession_id_validation_error = "Invalid Accession ID, ensure validity of Accession ID  & absence of special characters or symbols in text."
text_field_overflow_validation_error = "Text should not be more than 3000 characters long"


# ----------------------------------------------------------------------------------------------------------------------
# Custom Form Validation Function
# ----------------------------------------------------------------------------------------------------------------------

def validate_format(form, field):
    """
    Validates the format of the protein sequence entered in the form field based on the selected sequence format.

    :param form: FlaskForm, the form object containing the protein sequence field and format radio button field.
    :param field: TextAreaField, the protein sequence field to be validated.
    :raises ValidationError: if the protein sequence format is invalid based on the selected format radio button.

    Note:
    - The function checks the selected sequence format radio button field to determine the expected format.
    - If the format is "fasta_sequence", the function validates the protein sequence field against the FASTA format pattern.
    - If the format is "plain_text", the function validates the protein sequence field against the plain text format pattern.
    - If the format is "ncbi_accession_id", the function validates the protein sequence field as an NCBI Accession ID.
    - For each format, if the validation fails, a ValidationError is raised with the corresponding error message.
    """
    if form.sequence_format_radio_button_field.data == "fasta_sequence":
        pattern = r"\s*>\S+(?: \S+)*\s+[ACDEFGHIKLMNPQRSTVWYacdefghiklmnpqrstvwy]+(?:\s+[ACDEFGHIKLMNPQRSTVWYacdefghiklmnpqrstvwy]+)*"
        if not re.fullmatch(pattern, field.data):
            raise ValidationError(fasta_format_validation_error)

    elif form.sequence_format_radio_button_field.data == "plain_text":
        pattern = r"^[ACDEFGHIKLMNPQRSTVWYacdefghiklmnpqrstvwy]+$"
        if not re.fullmatch(pattern, field.data):
            raise ValidationError(text_format_validation_error)

    elif form.sequence_format_radio_button_field.data == "ncbi_accession_id":
        ncbi_accession_id = form.protein_sequence_field.data.strip()
        url = f"https://www.ncbi.nlm.nih.gov/sviewer/viewer.fcgi?id={ncbi_accession_id}&db=protein&report=fasta"
        if (requests.get(url).status_code != 200) or (not requests.get(url).text.startswith(">")):
            raise ValidationError(ncbi_accession_id_validation_error)


# def validate_min_window_length(form, field):
#     print(form.protein_sequence_field.data)
#     print(field.data)
#     if form.sequence_format_radio_button_field.data == "ncbi_accession_id":
#         ncbi_accession_id = form.protein_sequence_field.data.strip()
#         url = f"https://www.ncbi.nlm.nih.gov/sviewer/viewer.fcgi?id={ncbi_accession_id}&db=protein&report=fasta"
#         sequence = requests.get(url).text
#     elif:
#         sequence = form.protein_sequence_field.data
#     if (len() * 2) < field.data:
#         raise ValidationError("Sequence Length Should be at least Double of Window Length")
#     else:
#         print("success")

# ----------------------------------------------------------------------------------------------------------------------
# Input Form Class
# ----------------------------------------------------------------------------------------------------------------------

class InputForm(FlaskForm):
    # Text area field for entering the protein sequence
    protein_sequence_field = TextAreaField(label="protein sequence",
                                           validators=[DataRequired(),
                                                       Length(max=3000, message=text_field_overflow_validation_error),
                                                       validate_format],
                                           render_kw={"placeholder": " Enter Your Text Here"})

    # Radio button field for selecting the sequence format
    sequence_format_radio_button_field = RadioField(label="Label",
                                                    choices=[
                                                        ("plain_text", "text"),
                                                        ("fasta_sequence", "fasta"),
                                                        ("ncbi_accession_id", "NCBI id"),
                                                    ],
                                                    default="fasta_sequence",
                                                    validators=[DataRequired()])

    # Range field for selecting the window length
    window_length_range_field = DecimalRangeField(label="window length",
                                                  validators=[DataRequired(),
                                                              NumberRange(min=3, max=29)],
                                                  default=7,
                                                  render_kw={"type": "range", "step": 2})

    # Range field for selecting the edge weight
    edge_weight_range_field = DecimalRangeField(label="edge weight",
                                                validators=[NumberRange(min=0, max=1)],
                                                default=1,
                                                render_kw={"type": "range", "step": 0.1})

    # Select box field for selecting the progression model
    model_select_field = SelectField(label="Model",
                                     choices=["Linear Progression",
                                              "Geometric Progression"],
                                     render_kw={"onchange": "getSelectedValue()"})

    # Submit button field
    submit_button_field = SubmitField("submit")
