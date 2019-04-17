from ask_sdk_model.interfaces.display import RenderTemplateDirective, BodyTemplate2, BackButtonBehavior, ImageInstance
from ask_sdk_model.ui import SimpleCard, StandardCard, Image
import dynamo_helper


def build_response(handler_input, card_title, card_text, speech_text, card_image_url=None, end_session=False):
    if handler_input.attributes_manager.session_attributes["drunk_mode_state"]:
        speech_text = '<prosody rate="x-slow"><emphasis level="strong">' + speech_text + '</emphasis></prosody>'

    if card_image_url:
        # card = StandardCard(card_title, card_text, Image(card_image_url, card_image_url))
        img = Image(sources=[ImageInstance(url=card_image_url)])
        directive = RenderTemplateDirective(
                    BodyTemplate2(
                        back_button=BackButtonBehavior.HIDDEN,
                        image=img, title=card_title,
                        text_content=card_text))
        handler_input.response_builder.speak(speech_text).add_directive(directive).set_should_end_session(end_session)
    else:
        card = SimpleCard(card_title, card_text)
        handler_input.response_builder.speak(speech_text).set_card(card).set_should_end_session(end_session)

    return handler_input.response_builder.response


def set_drunk_mode(user_id, handler_input, state):
    dynamo_helper.set_col_val(user_id, "drunk_mode_state", state)
    handler_input.attributes_manager.session_attributes["drunk_mode_state"] = state


def get_drunk_mode_state(user_id):
    response = dynamo_helper.get_item_from_users(user_id)
    if 'Item' in response and 'drunk_mode_state' in response['Item']:
        return response['Item']['drunk_mode_state']
    else:
        return False
