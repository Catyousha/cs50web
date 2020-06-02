document.addEventListener('DOMContentLoaded', () =>{

    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
    socket.on('connect', () => {

        document.querySelector('#newchannel-submit').onclick = () => {
            const newchannel = document.querySelector('#newchannel-name').value;
            socket.emit('submit new channel', {'newchannel-name': newchannel});
        };
    });

    socket.on('new channel added', data =>{
        const ch = document.createElement('a');
        ch.innerHTML = `# ${data.newch}`;
        ch.href = `${window.location.origin}/channels/${data.newch}`;
        ch.classList.add("list-group-item");
        ch.classList.add("list-group-item-action");
        document.querySelector('#channels').append(ch);
    });
});