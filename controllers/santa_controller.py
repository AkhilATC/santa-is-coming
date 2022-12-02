from flask import Blueprint, jsonify, request, current_app, render_template
from data_layer.data_container import ques

santa = Blueprint("santa-mod",__name__,url_prefix="/santa-is-coming")


def fetch_template(q=0):
    url_end = "/santa-is-coming/santa-in-action"
    if not q:
        d = list(filter(lambda x: x['id'] == int(1), ques))[0]
        rendering_template = f"<form action='{url_end}' method='POST'>" \
                             f"<p> {d['questions']} <input type = 'text' name='{q+1}'/></p>"\
                             "<button name='forwardBtn' type='submit'>🏁</button></form>"
        return rendering_template
    else:
        q_id = int(q[0])
        ans = str(q[1]).lower()
        print(q_id)
        d = list(filter(lambda x: x['id'] == q_id and x['ans'] == ans, ques))
        print("------------->>>>>")
        print(d)
        if q_id == 5 and d:
            return "Congrats, സെർവർ റൂമിന് സമീപം എവിടെയെങ്കിലും സൈഫറിന്റെ ഒരു ഭാഗം കണ്ടെത്തുക"
        if not d:
            d = list(filter(lambda x: x['id'] == int(1), ques))[0]
            rendering_template = f"<form action='{url_end}' method='POST'>" \
                                 f"<p> {d['questions']} <input type = 'text' name='{0 + 1}'/></p>" \
                                 "<button name='forwardBtn' type='submit'>🏁</button></form>"
            return rendering_template
        next_ = list(filter(lambda x: x['id'] == int(q_id + 1), ques))[0]
        rendering_template = f"<form action='{url_end}' method='POST'>" \
                             f"<p> {next_['questions']} <input type = 'text' name='{q_id + 1}'/></p>" \
                             "<button name='forwardBtn' type='submit'>🏁</button></form>"
        return rendering_template




@santa.route("/")
def render():
    return render_template("main_template.html")


@santa.route("/santa-in-action",methods=['POST'])
def santa_in_action():
    result = request.form
    ans = [x for x in result.items() if x[0] != 'forwardBtn']
    print(ans)
    ans = ans[0] if len(ans) == 1 else 0
    print(ans)
    return render_template("render.html",render=fetch_template(q=ans))

@santa.route("/<q_id>/submit-answer", methods=['POST'])
def submit_answer(q_id):
    try:
        ans = request.json
        answer = ans['answer'],
        d = list(filter(lambda x: x['id'] == int(q_id) and x['ans'] == answer, ques))
        if not d:
            return jsonify({"message": "wrong"}), 400
        return jsonify({
            "message": "success",
            "next_questions": list(filter(lambda x: x['id'] == int(q_id+1), ques)),
            "code": current_app.get("code") if q_id == 5 else None
        })
    except Exception as e:
        return jsonify({
            "message": "Failed to submit answer",
            "data": []
        }), 400