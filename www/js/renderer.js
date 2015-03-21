define(["utils", "pixi", "fpsmeter", "viewport"], function (Utils, PIXI, FPSMeter, ViewPort) {
    var Renderer = Utils.extend(null, {
        cls: "Renderer",

        create: function create(game) {
            var _this = Object.create(this);
            _this.initialize(game);
            return _this;
        },

        initialize: function initialize(game) {
            this.game = game;
            this.staticElements = {};
            this.elements = {};
            this.backgroundColor = 0x020025;

            this.worldLimits = null;

            this.move = {x: 0, y: 0};
            this.resolution = {
                width: null,
                height: null,
                aspectRatio: null
            };

            this.resize(true);
            this.initPixi();

            this.meter = new FPSMeter({
                show: 'fps',
                toggleOn: 'click',
                theme: 'colorful',
                smoothing: 3,
                graph: 1
            });
        },

        worldUpdated: function worldUpdated() {
            this.worldLimits = {
                minX: this.game.world.width * -0.5,
                maxX: this.game.world.width * 0.5,
                minY: this.game.world.height * -0.5,
                maxY: this.game.world.height * 0.5
            };

            this.worldLimits.width = Math.abs(this.worldLimits.minX - this.worldLimits.maxX);
            this.worldLimits.height = Math.abs(this.worldLimits.minY - this.worldLimits.maxY);

            if (!this.viewport) {
                this.viewport = ViewPort.create(this, this.worldLimits, this.resolution);
            } else {
                this.viewport.move(0, 0);
            }
        },

        loadTextures: function loadTexture() {
            var assets = ["star"];

            this.textures = {};

            for (var i = 0, count = assets.length; i < count; i += 1) {
                var id = assets[i];
                this.textures[id] = PIXI.Texture.fromImage(
                    this.game.getImage(id)
                );
            }

        },

        initPixi: function initPixi() {
            Utils.log("Renderer.initPixi");
            // create an new instance of a pixi stage
            this.stage = new PIXI.Stage(this.backgroundColor, true);

            this.staticElements.viewportWidth = new PIXI.Text("", {
                font: "bold 20px Arial",
                fill: "white",
                align: "left",
                stroke: "black",
                strokeThickness: 2,
            });

            this.staticElements.viewportWidth.position.x = 450;
            this.staticElements.viewportWidth.position.y = 5;

            this.staticElements.gameTime = new PIXI.Text("", {
                font: "bold 20px Arial",
                fill: "white",
                align: "left",
                stroke: "black",
                strokeThickness: 2,
            });

            this.staticElements.gameTime.position.x = 450;
            this.staticElements.gameTime.position.y = 25;

            // create a renderer instance.
            this.pixiRenderer = PIXI.autoDetectRenderer(
                this.resolution.width,
                this.resolution.height,
                {
                    antialiasing: false,
                    transparent: false,
                    resolution: window.devicePixelRatio
                }
            );

            // add the renderer view element to the DOM
            document.body.appendChild(this.pixiRenderer.view);

            this.resize();
            window.addEventListener("resize", function () {
                this.resize();
            }.bind(this));

            this._registerMapDrag();
            this._registerMapZoom();
        },

        resize: function resize(skipPixi) {
            var width = window.innerWidth;
            var height = window.innerHeight;

            this.resolution.width = width;
            this.resolution.height = height;
            this.resolution.aspectRatio = width / height;

            if (this.viewport) {
                this.viewport.resize();
            }

            if (!skipPixi) {
                Utils.log("Resized PIXI renderer to " + width + "x" + height);
                this.pixiRenderer.resize(width, height);
            }
        },

        setViewportWidth: function setViewportWidth(lightseconds) {
            this.staticElements.viewportWidth.setText(Utils.distanceToText(lightseconds));
        },

        _registerMapDrag: function _registerMapDrag() {
            var prev = null;
            var dragging = false;
            var renderer = this;

            this.stage.mousedown = this.stage.touchstart = function (data) {
                prev = {
                    x: data.global.x,
                    y: data.global.y
                };

                dragging = true;
            };

            this.stage.mouseup = this.stage.mouseupoutside = this.stage.touchend = function (data) {
                prev = null;
                dragging = false;
            };

            this.stage.mousemove = this.stage.touchmove = function (data) {
                if (dragging && prev) {
                    var x = prev.x - data.global.x;
                    var y = prev.y - data.global.y;

                    renderer.move.x += x;
                    renderer.move.y += y;
                }

                prev = {
                    x: data.global.x,
                    y: data.global.y
                };
            };
        },

        _registerMapZoom: function _registerMapZoom() {
            var renderer = this;

            function _distance(event) {
                var wheelDelta = event.wheelDelta, detail = event.detail;
                if (detail) {
                    if (wheelDelta) { // Opera
                        return wheelDelta / detail / 40 * detail > 0 ? 1 : -1;
                    }
                    else { // Firefox;         TODO: do not /3 for OS X
                        return -detail / 3;
                    }
                } else { // IE/Safari/Chrome TODO: /3 for Chrome OS X;
                    return wheelDelta / 120;
                }
            }

            function _onScroll(data) {
                if (!data) {
                    data = event;
                }

                var distance = _distance(data);

                renderer.viewport.zoom(distance);
            }

            document.addEventListener("DOMMouseScroll", _onScroll, false);
            document.addEventListener("mousewheel", _onScroll, false);
        },

        tick: function tick() {
            if (this.move.x || this.move.y) {
                var move = this.move;
                this.move = {x: 0, y: 0};
                this.viewport.movePixels(move.x, move.y);
            }

            this._recalculateDynamicElements();

            this.stage.addChild(this.staticElements.viewportWidth);
            this.stage.addChild(this.staticElements.gameTime);

            this.elements.viewportWidth = this.staticElements.viewportWidth;
            this.elements.gameTime = this.staticElements.gameTime;

            this.pixiRenderer.render(this.stage);
            this.meter.tick();
        },

        _recalculateDynamicElements: function _recalculateDynamicElements() {
            if (this.worldLimits === null) {
                return;
            }

            for (var id in this.elements) {
                this.stage.removeChild(this.elements[id]);
            }

            var vp = this.viewport;

            var stars = 0;
            for (var id in this.game.world.stars) {
                var star = this.game.world.stars[id];

                // Skip stars outside viewport
                if (star.x < vp.minX || star.x > vp.maxX ||
                    star.y < vp.minY || star.y > vp.maxY) {
                    continue;
                }

                try {
                    var pos = this._worldToRenderer(star.x, star.y);
                } catch (e) {
                    console.error("Error with star:");
                    console.dir(star);
                    throw e;
                }

                var element = new PIXI.Sprite(this.textures.star);

                element.position.x = pos.x;
                element.position.y = pos.y;

                element.anchor.x = 0.5;
                element.anchor.y = 0.5;

                element.rotation = star.rotation;

                this.elements[id] = element;
                this.stage.addChild(element);

                stars++;
            }

            // console.log("Rendering " + stars + " stars");
        },

        _translate: function _translate(pos, min, max, rendererMax) {

            if (pos < min || pos > max) {
                throw new Error("Trying to translate out of bounds coords!");
            }

            var distance = Math.abs(min - max);
            var newPos = pos - min;
            var relativePos = newPos / distance;

            return relativePos * rendererMax;
        },

        _worldToRenderer: function _worldToRenderer(worldX, worldY) {
            return {
                x: this._translate(
                    worldX,
                    this.viewport.minX,
                    this.viewport.maxX,
                    this.resolution.width
                ),
                y: this._translate(
                    worldY,
                    this.viewport.minY,
                    this.viewport.maxY,
                    this.resolution.height
                )
            }
        }
    });

    return Renderer;
})