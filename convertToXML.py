import pandas as pd

question_types = [
    {
        "name": "Multiple Choice",
        "type": "kprime"
    },
    {
        "name": "Fill in the Blanks",
        "type": "multichoice"
    },
    {
        "name": "Match the Following",
        "type": "matching"
    },
    {
        "name": "TrueFalse",
        "type": "truefalse"
    },
]

from xml.etree.ElementTree import Element, SubElement, Comment

from xml.etree import ElementTree
from xml.dom import minidom


def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")


# Configure one attribute with set()

root = Element('quiz')

for question_type in question_types:
    data = pd.read_excel('Moodle Bulk Import Format.xlsx', sheet_name=question_type['name'])
    if question_type['type'] == 'matching':
        data = data.groupby('Sr. No.', as_index=False)
    else:
        data = data.iterrows()
    for _, d in data:
        question = Element('question', {'type': question_type['type']})
        SubElement(question, 'shuffleanswers').text = 'true'
        SubElement(question, 'idnumber').text = ''
        SubElement(question, 'hidden').text = '0'
        if question_type['type'] == 'kprime':
            SubElement(SubElement(question, 'name'), 'text').text = str(d['Question'])
            SubElement(SubElement(question, 'questiontext'), 'text').text = str(d['Question'])
            SubElement(question, 'penalty').text = '0.3333333'
            SubElement(SubElement(question, 'generalfeedback'), 'text').text = str(d['Feedback'])
            SubElement(question, 'defaultgrade').text = '4.0000000'
            SubElement(SubElement(question, 'scoringmethod'), 'text').text = 'subpoints'
            SubElement(question, 'numberofrows').text = '4'
            SubElement(question, 'numberofcolumns').text = '2'
            for i in range(1, 5):
                row = SubElement(question, 'row', {'number': str(i)})
                SubElement(SubElement(row, 'optiontext'), 'text').text = str(d['Option {0}'.format(i)])
                SubElement(SubElement(row, 'feedbacktext'), 'text').text = str(d['Option {0} Feedback'.format(i)])
            SubElement(SubElement(SubElement(question, 'column', {'number': '1'}), 'responsetext', {'format': 'moodle_auto_format'}), 'text').text = 'True'
            SubElement(SubElement(SubElement(question, 'column', {'number': '2'}), 'responsetext', {'format': 'moodle_auto_format'}), 'text').text = 'False'
            for i in range(1, 5):
                SubElement(SubElement(question, 'weight', {'rownumber': str(i), 'columnnumber': '1'}), 'value').text = '1.000' if d['Option {0} Answer'.format(i)] else '0.000'
                SubElement(SubElement(question, 'weight', {'rownumber': str(i), 'columnnumber': '2'}), 'value').text = '0.000' if d['Option {0} Answer'.format(i)] else '1.000'
        elif question_type['type'] == 'multichoice':
            SubElement(SubElement(question, 'name'), 'text').text = str(d['Question'])
            SubElement(SubElement(question, 'questiontext'), 'text').text = str(d['Question'])
            SubElement(question, 'penalty').text = '0.3333333'
            SubElement(SubElement(question, 'generalfeedback'), 'text').text = str(d['Feedback'])
            SubElement(question, 'defaultgrade').text = '{0}.0000000'.format(int(d['Marks']))
            SubElement(question, 'single').text = 'true'
            SubElement(question, 'answernumbering').text = 'abc'
            SubElement(question, 'showstandardinstruction').text = '0'
            SubElement(SubElement(question, 'correctfeedback'), 'text').text = 'Your answer is correct.'
            SubElement(SubElement(question, 'partiallycorrectfeedback'), 'text').text = 'Your answer is partially correct.'
            SubElement(SubElement(question, 'incorrectfeedback'), 'text').text = 'Your answer is incorrect.'
            SubElement(question, 'shownumcorrect').text = ''
            for i in range(1, 5):
                answer = SubElement(question, 'answer', {'fraction': '100' if 'Option {0}'.format(i) == str(d['Answer']) else '0'})
                SubElement(answer, 'text').text = str(d['Option {0}'.format(i)])
                SubElement(SubElement(answer, 'feedback'), 'text').text = str(d['Option {0} Feedback'.format(i)])
        elif question_type['type'] == 'matching':
            SubElement(SubElement(question, 'name'), 'text').text = str(d['Question Name'].iloc[0])
            SubElement(SubElement(question, 'questiontext'), 'text').text = str(d['Question Name'].iloc[0])
            SubElement(question, 'penalty').text = '0.3333333'
            SubElement(SubElement(question, 'correctfeedback'), 'text').text = 'Your answer is correct.'
            SubElement(SubElement(question, 'partiallycorrectfeedback'), 'text').text = 'Your answer is partially correct.'
            SubElement(SubElement(question, 'incorrectfeedback'), 'text').text = 'Your answer is incorrect.'
            SubElement(question, 'shownumcorrect').text = ''
            for _, q in d.iterrows():
                subquestion = SubElement(question, 'subquestion')
                SubElement(subquestion, 'text').text = str(q['Question'])
                SubElement(SubElement(subquestion, 'answer'), 'text').text = str(q['Answer'])
        elif question_type['type'] == 'truefalse':
            SubElement(SubElement(question, 'name'), 'text').text = str(d['Question'])
            SubElement(SubElement(question, 'questiontext'), 'text').text = str(d['Question'])
            SubElement(SubElement(question, 'generalfeedback'), 'text').text = str(d['Feedback'])
            SubElement(question, 'defaultgrade').text = '1.0000000'
            SubElement(question, 'penalty').text = '1.0000000'
            true_answer = SubElement(question, 'answer', {
                'fraction': '100' if d['Answer'] else '0',
                'format': 'moodle_auto_format'
            })
            SubElement(true_answer, 'text').text = 'true'
            SubElement(SubElement(true_answer, 'feedback'), 'text').text = str(d['Feedback for True'])
            false_answer = SubElement(question, 'answer', {
                'fraction': '0' if d['Answer'] else '100',
                'format': 'moodle_auto_format'
            })
            SubElement(false_answer, 'text').text = 'false'
            SubElement(SubElement(false_answer, 'feedback'), 'text').text = str(d['Feedback for False'])
        else:
            continue
        root.append(question)

print(prettify(root))
