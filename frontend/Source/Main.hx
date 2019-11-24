package;

import openfl.display.Sprite;
import openfl.text.TextField;
import openfl.text.TextFieldType;
import openfl.text.TextFormat;
import openfl.events.Event;
import openfl.events.MouseEvent;
import openfl.events.TouchEvent;
import motion.Actuate;
import motion.easing.Elastic;

class Main extends Sprite
{

  var text: TextField;
  var request_in_process: Bool = false;

  public function new()
  {
    super();
    init();
  }

  public function init():Void {
    text = new TextField();
    text.selectable = true;
    text.type = TextFieldType.INPUT;
    text.border = true;
    text.borderColor = 0x0f0f0f;
    addChild(text);
    render_input();
    text.addEventListener(Event.ENTER_FRAME, loop);    

  }

  private function loop(e: Event)
  {
    if(text.text.length == 11 && request_in_process == false) {
      make_request();
    }
  }

  private function render_response(opsos:String, location:String)
  {
    trace("render response");
    text.multiline = true;
    text.restrict = null;
    text.height = stage.stageHeight / 3;
    text.width = stage.stageWidth / 1.2;
    text_field_reposition();
    var textFormat = new TextFormat(null, Std.int(text.height / 5));
    text.setTextFormat(textFormat);
    if (opsos == "Not found" && location == "Not found"){
      text.text = "Номер должен быть в формате: \n7987654321.";
    } else {
      text.text = opsos + "\n" + location;      
    }
    text.addEventListener(MouseEvent.MOUSE_DOWN, click_after_render_response);
    text.addEventListener(TouchEvent.TOUCH_BEGIN, touch_after_render_response);
  }

  private function click_after_render_response(e) {
    text.removeEventListener(MouseEvent.MOUSE_DOWN, click_after_render_response);
    text.removeEventListener(TouchEvent.TOUCH_BEGIN, touch_after_render_response);
    render_input();
  }

  private function touch_after_render_response(e) {
    text.removeEventListener(MouseEvent.MOUSE_DOWN, click_after_render_response);
    text.removeEventListener(TouchEvent.TOUCH_BEGIN, touch_after_render_response);
    render_input();
  }

  private function render_input()
  {
    text.text = "";
    text.multiline = false;
    text.restrict = "0-9";
    text.maxChars = 11;
    text.width = stage.stageWidth / 1.5;
    text.height = stage.stageHeight / 6;
    text_field_reposition();
    var textFormat = new TextFormat(null, Std.int(text.height - 5));
    text.setTextFormat(textFormat);
    request_in_process = false;
  }

  private function text_field_reposition()
  {

    var nX = (stage.stageWidth - text.width) / 2;
    var nY = (stage.stageHeight - text.height) / 2;
    Actuate.tween (text, 2, {y: nY}).ease(Elastic.easeOut);
    Actuate.tween (text, 2, {x: nX}).ease(Elastic.easeOut);
  }
  
  private function make_request()
  {
    request_in_process = true;
    Actuate.tween (text, 0, {y: -1000});
    trace("make request");
    var http = new haxe.Http("https://numbers.gaag.site/numberdetect/" + text.text);
    http.onData = function (data: String) {
	var result = haxe.Json.parse(data);
        trace(result);
	render_response(result.location, result.opsos);
    }
    http.onError = function (error) {
	trace('error $error');
	render_response("Not found", "Not found");
    }
    http.request();
  }

}
