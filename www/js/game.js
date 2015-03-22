define([
    "sockjs", "utils", "messages", "world", "renderer", "player"
], function (SockJS, Utils, Messages, World, Renderer, Player) {

    var assets = {
        "yellow-dwarf": {src: "assets/images/star.png"},
        "red-dwarf": {src: "assets/images/red-dwarf.png"},
        "red-giant": {src: "assets/images/red-giant.png"},
        "blue-giant": {src: "assets/images/blue-giant.png"},
        "space-ship": {src: "assets/images/space-ship.png"},
    };

    var volumes = {
        "general": 0.1,
        "sfx": 0.1
    };

    var Game = function () {
        this.initialize();
    };

    Game.prototype = {
        initialize: function initialize() {
            Utils.log("Game.initialize");
            this.queue = null;
            this.gameTime = 0;

            this.world = World.create(this);
            this.renderer = Renderer.create(this);
            this.player = Player.create(this.getPlayerId());
        },

        start: function start() {
            Utils.log("Game.start");
            this.queue = new createjs.LoadQueue(true);
            this.queue.installPlugin(createjs.Sound);
            this.queue.on("progress", this._loadProgress, this);
            this.queue.on("complete", this._loadComplete, this);

            var manifest = [];
            for (var key in assets) {
                var item = assets[key];
                item.id = key;
                manifest.push(item);
            }

            if (manifest.length > 0) {
                this.queue.loadManifest(manifest);
            } else {
                this._loadComplete();
            }
        },

        setup: function setup() {
            Utils.log("Game.setup");
            this._connect();

            this.tick();
        },

        tick: function tick() {
            this.renderer.tick();
            window.requestAnimationFrame(this.tick.bind(this));
        },

        playSound: function playSound(id) {
            Utils.log("Game.playSound(" + id + ")");
            var sound = createjs.Sound.play(id);
            var category = assets[id].category;

            if (!volumes[category]) {
                throw new Error("No volume for category " + category);
            }

            sound.volume = volumes[category];
        },

        getImage: function getImage(id) {
            Utils.log("Game.getImage(" + id + ")");
            var res = this.queue.getResult(id);
            if (!res) {
                throw new Error("Invalid image ID " + id);
            }
            return res.src;
        },

        setGameTime: function setGameTime(time) {
            this.gameTime = time;
            this.renderer.staticElements.gameTime.setText(Utils.timeToText(time));
        },

        setWorldData: function setWorldData(data) {
            this.world.setData(data);
            this.renderer.worldUpdated();
        },

        setPlayerId: function setPlayerId(id) {
            localStorage.setItem("playerId", id);
            this.player.id = id;
        },

        getPlayerId: function getPlayerId() {
            return localStorage.getItem("playerId");
        },

        _registerPlayer: function _registerPlayer() {
            var id = this.getPlayerId();

            Utils.log("Registering player ID " + id);

            this.connection.send(JSON.stringify({
                "type": "RegisterPlayer",
                "player_id": id
            }));
        },

        _connect: function _connect() {
            Utils.log("Game._connect");

            var url = "/api/game";
            this.connection = new SockJS(url);
            this.connection.onopen = this._onOpen.bind(this);
            this.connection.onmessage = this._onMessage.bind(this);
            this.connection.onclose = this._onClose.bind(this);
        },

        _onOpen: function _onOpen(event) {
            console.log("Connection established");
            this._registerPlayer();
        },

        _onMessage: function _onOpen(event) {
            var messages = JSON.parse(event.data);
            var game = this;
            messages.forEach(function (data) {
                try {
                    if (!(data.type in Messages)) {
                        throw new Error("Unknown message type " + data.type);
                    }

                    var message = Messages[data.type].create(game, data);

                    setTimeout(function () {
                        message.process();
                    }, 0);
                } catch (err) {
                    console.log("Caught " + err + " when processing messages");
                    console.log(err.stack);
                    console.dir(messages);
                }
            });
        },

        _onClose: function _onOpen(event) {
            console.log("Connection to server severed", event);
            setTimeout(function () {
                console.log("Reconnecting...");
                this._connect();
            }.bind(this), 500);
        },

        _loadProgress: function _loadProgress(event) {
            var pct = (event.loaded * 100);
            console.log('Load progress: ' + pct + "%");
        },

        _loadComplete: function _loadComplete() {
            this.setup();
        }
    };

    return new Game();
});