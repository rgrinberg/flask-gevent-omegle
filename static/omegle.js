var url = "ws://localhost:8000/ws";
var client = {
    ws: null,
    send: function () {
        if (!this.ws){
           console.log("Please connect before sending");
        } else {
            var msg = this.message();
            this.ws.send(msg);
            this.appendChat("You: " + msg);
        }
    },
    close: function () {
        if(this.ws) {
            this.ws.close();
        }
        ws = null;
    },
    seek: function() {
        if (this.ws) {
            this.disconnect();
        }
        var ws = new WebSocket(url);
        var self = this;
        this.ws = ws;
        ws.onmessage = function (evt) {
            if (evt.data.charAt(0) == '/') { // server message
                self.appendChat("*** " + evt.data.substr(1, evt.data.length - 1) + " ***");
            } else {
                self.appendChat("Stranger: " + evt.data);
            }
        };
        ws.onclose = function (evt) {
            self.appendChat("disconnected");
        };
    },
    message: function () {
        return document.getElementById("send_message").value;
    },
    appendChat: function (message) {
        messages.innerHTML = messages.innerHTML + "<br/>" + message;
    }
};
