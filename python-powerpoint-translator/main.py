from flask import Flask, request, send_file, render_template
from pptx import Presentation
from googletrans import Translator
import os
import tempfile

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('upload_form.html')

def translate_to_spanish(text):
    translator = Translator()
    translated = translator.translate(text, src='en', dest='es')
    return translated.text

def translate_presentation(input_path, output_path):
    prs = Presentation(input_path)
    i = False

    for slide in prs.slides:
        for shape in slide.shapes:
            if hasattr(shape, "text"):
                original_text = shape.text
                if str(original_text) != '' and original_text is not None:
                    for char in str(original_text):
                        if char.isalnum():
                            i = True
                            break
                    if i:
                        translated_text = translate_to_spanish(original_text)
                        shape.text = translated_text
                        i = False

    prs.save(output_path)


@app.route('/translate', methods=['POST'])
def translate_pptx_and_return():
    uploaded_file = request.files['file']

    if uploaded_file.filename != '':
        # Create a temporary directory to save the uploaded file
        temp_dir = tempfile.mkdtemp()
        uploaded_path = os.path.join(temp_dir, uploaded_file.filename)
        uploaded_file.save(uploaded_path)

        ppt_name = os.path.splitext(uploaded_file.filename)[0]
        output_path = os.path.join(temp_dir, f"{ppt_name}-translated(es).pptx")

        translate_presentation(uploaded_path, output_path)

        return send_file(output_path, as_attachment=True, download_name=f"{ppt_name}-translated(es).pptx")

    return "No file uploaded"

if __name__ == "__main__":
    app.run(debug=True)

# from pptx import Presentation
# from googletrans import Translator
#
#
# def translate_to_spanish(text):
#     translator = Translator()
#     translated = translator.translate(text, src='en', dest='es')
#     return translated.text
#
#
# def translate_presentation(input_path, output_path):
#     prs = Presentation(input_path)
#     i = False
#
#     for slide in prs.slides:
#         for shape in slide.shapes:
#             if hasattr(shape, "text"):
#                 original_text = shape.text
#                 if str(original_text) != '' and original_text is not None:
#                     for char in str(original_text):
#                         if char.isalnum():
#                             i = True
#                             break
#                     if i:
#                         translated_text = translate_to_spanish(original_text)
#                         shape.text = translated_text
#                         i = False
#
#     prs.save(output_path)
#
#
# if __name__ == "__main__":
#     ppt_name = "8_14_Origin_of_the_Universe"
#     input_pptx = ppt_name + ".pptx"
#     output_pptx = ppt_name + "-translated(es).pptx"
#
#     translate_presentation(input_pptx, output_pptx)
