from __future__ import annotations
from flask import render_template, url_for
from prolign import app
from prolign.forms import InputForm
from prolign.fetch_utils import ncbi_sequence_fetcher
from prolign.parse_utils import fasta_sequence_parser, text_sequence_parser
from prolign.alignment_generator import needleman_wunsch_global_alignment


# ----------------------------------------------------------------------------------------------------------------------
# Home Route
# ----------------------------------------------------------------------------------------------------------------------

@app.route("/", methods=["GET", "POST"])
@app.route("/home", methods=["GET", "POST"])
def home():
    # Load input-form object
    form_object = InputForm()

    # Check form validation
    if form_object.validate_on_submit():

        # Set global variables
        user_protein_sequence: str | None = None
        user_protein_sequence_name: str | None = None

        # Get user input from the form
        user_text_area_input: str = form_object.protein_sequence_field.data
        user_protein_sequence_format_choice: str = form_object.sequence_format_radio_button_field.data
        user_window_length_input: int = int(form_object.window_length_range_field.data)
        user_edge_weight_input: float = float(form_object.edge_weight_range_field.data)
        user_model_selection_input: str = form_object.model_select_field.data.split(" ")[0]

        # Fetch sequence
        if user_protein_sequence_format_choice == "ncbi_accession_id":
            # Fetch protein sequence from NCBI using the provided accession ID
            user_protein_sequence: str = ncbi_sequence_fetcher(user_text_area_input)
        else:
            # Use the user-provided protein sequence directly
            user_protein_sequence: str = user_text_area_input

        print(user_model_selection_input)
        # Parse sequence
        if user_protein_sequence_format_choice == "ncbi_accession_id":
            user_protein_sequence_name, user_protein_sequence = fasta_sequence_parser(user_protein_sequence,
                                                                                      fetched=True)
        elif user_protein_sequence_format_choice == "fasta_sequence":
            user_protein_sequence_name, user_protein_sequence = fasta_sequence_parser(user_protein_sequence,
                                                                                      fetched=False)
        elif user_protein_sequence_format_choice == "plain_text":
            user_protein_sequence = text_sequence_parser(user_protein_sequence)

        # Generate Alignment
        aligment_array = needleman_wunsch_global_alignment(protein_sequence=user_protein_sequence,
                                                                  window_length=user_window_length_input,
                                                                  edge_weight=user_edge_weight_input,
                                                                  method=user_model_selection_input)


        # Render the template with the generated Alignment
        return render_template("index.html",
                               title="Home",
                               form=form_object,
                               alignment=aligment_array)

    else:
        print("Invalid")

    # Render the template with the input form
    return render_template("index.html",
                           title="Home",
                           form=form_object)


# ----------------------------------------------------------------------------------------------------------------------
# Documentation Route
# ----------------------------------------------------------------------------------------------------------------------


@app.route("/documentation", methods=["GET"])
def documentation():
    return render_template("documentation.html",
                           title="Documentation")
