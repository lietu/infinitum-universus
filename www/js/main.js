(function() {
    require.config({
        baseUrl: "js/",
        paths: {
            "fpsmeter": "lib/fpsmeter/dist/fpsmeter",
            "pixi": "lib/pixi.js/bin/pixi.dev",
            "sockjs": "lib/sockjs/sockjs",
            "lodash": "lib/lodash/lodash",
            "rivets": "lib/rivets/dist/rivets",
            "sightglass": "lib/sightglass/index",
            "moment": "lib/momentjs/moment"
        },
        shim: {
            "fpsmeter": {
                exports: 'FPSMeter'
            }
        },
        waitSeconds: 15
    });

    require(["game"], function (game) {
        game.start();
    })
})();
