document.addEventListener('DOMContentLoaded', () =>{

    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
    socket.on('connect', () => {

        let chatMsg = document.querySelector('#chatMsg');
        if (chatMsg){
            socket.emit('user enter channel');
            window.addEventListener("beforeunload", (event) =>{
                socket.emit('user leave channel');
            });
        };

        let newchannel_submit = document.querySelector('#newchannel-submit');
        if (newchannel_submit){
            newchannel_submit.addEventListener("click", () => {
                let err = document.querySelector("#error-text");
                if(err){
                    err.remove();
                };
                const newchannel = document.querySelector('#newchannel-name').value;
                document.querySelector('#newchannel-name').value = '';
                socket.emit('submit new channel', {'newchannel-name': newchannel});
            });
        };

        let msg_submit = document.querySelector('#msg-submit');
        if (msg_submit){

            msg_submit.addEventListener("click", () => {
                const msg = document.querySelector('#msg-text').value;
                document.querySelector('#msg-text').value = '';
                if(msg.length > 0){
                    socket.emit('submit message', {'message-text': msg});
                };
            });

            let msg_text = document.querySelector('#msg-text');
            msg_text.addEventListener("keyup", (e) =>{
                if(e.key == "Enter"){
                    msg_submit.click();
                };
            });

        };

    });

    socket.on('new channel added', data => {
        const ch = document.createElement('a');
        ch.innerHTML = `# ${data.newch}`;
        ch.href = `${window.location.origin}/channels/${data.newch}`;
        ch.classList.add("list-group-item");
        ch.classList.add("list-group-item-action");
        document.querySelector('#channels').append(ch);
        
    });

    socket.on('error add channel', data => {
        const err = document.createElement('p');
        err.innerHTML = `${data.error}`;
        err.classList.add("text-danger");
        err.setAttribute("id", "error-text");
        
        let ch_form = document.querySelector("#channel-form");
        let parentDiv = ch_form.parentNode;
        parentDiv.insertBefore(err, ch_form);
    });

    socket.on('user join chat', data => {
        const announce = document.createElement('p');
        announce.innerHTML = `[${data.timestamp}] <strong style="color: #${data.color};">${data.user} joined the chat`;
        document.querySelector('#chatMsg').append(announce);
    })

    socket.on('user leave chat', data => {
        const announce = document.createElement('p');
        announce.innerHTML = `[${data.timestamp}] <strong style="color: #${data.color};">${data.user} leave the chat`;
        document.querySelector('#chatMsg').append(announce);
    })

    socket.on('put message', data => {
        const newMsg = document.createElement('p');
        newMsg.innerHTML = `[${data.timestamp}] &lt;<strong style="color: #${data.color};">${data.user}</strong>&gt; ${data.msg}`;
        document.querySelector('#chatMsg').append(newMsg);

    });
});