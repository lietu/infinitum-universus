define(["utils"], function (Utils) {
    var ViewPort = Utils.extend(null, {
        cls: "ViewPort",

        create: function create(renderer, worldLimits, resolution) {
            var _this = Object.create(this);
            _this.initialize(renderer, worldLimits, resolution);
            return _this;
        },

        initialize: function initialize(renderer, worldLimits, resolution) {
            this.renderer = renderer;
            this.worldLimits = worldLimits;
            this.resolution = resolution;
            this.setDefaults();
        },

        setDefaults: function setDefaults() {
            this.centerX = 0;
            this.centerY = 0;
            this.zoomFactor = 0.05;

            this.width = Math.abs(
                this.worldLimits.minX - this.worldLimits.maxX
            ) / 4;

            this.resize();

            this.renderer.setViewportWidth(this.width);

            this.updateLimits();
        },

        resize: function resize() {
            this.height = this.width / this.resolution.aspectRatio;
            this.updateLimits();

            var width = Utils.distanceToText(this.width);
            var height = Utils.distanceToText(this.height);

            Utils.log("Viewport resized to cover " + width + " x " + height);
        },

        zoom: function zoom(distance) {
            var zoomDistance = (this.zoomFactor * Math.abs(distance));

            if (distance < 0) {
                this.width = this.width + (this.width * zoomDistance);
            } else {
                this.width = this.width - (this.width * zoomDistance);
            }

            if (this.width > this.worldLimits.width) {
                this.width = this.worldLimits.width;
            }

            this.height = this.width / this.resolution.aspectRatio;

            this.renderer.setViewportWidth(this.width);

            this.move(0, 0);
        },

        movePixels: function movePixels(x, y) {
            this.move(
                x * this.lightSecondsPerPixel,
                y * this.lightSecondsPerPixel
            );
        },

        move: function move(x, y) {
            this.centerX += x;
            this.centerY += y;

            var minX = this.worldLimits.minX + this.width / 2;
            var maxX = this.worldLimits.maxX - this.width / 2;

            var minY = this.worldLimits.minY + this.height / 2;
            var maxY = this.worldLimits.maxY - this.height / 2;

            if (this.centerX < minX) {
                this.centerX = minX;
            } else if (this.centerX > maxX) {
                this.centerX = maxX;
            }

            if (this.centerY < minY) {
                this.centerY = minY;
            } else if (this.centerY > maxY) {
                this.centerY = maxY;
            }

            this.updateLimits();
        },

        updateLimits: function updateLimits() {
            this.lightSecondsPerPixel = this.width / this.resolution.width;

            this.minX = this.centerX + (this.width * -0.5);
            this.maxX = this.centerX + (this.width * 0.5);

            this.minY = this.centerY + (this.height * -0.5);
            this.maxY = this.centerY + (this.height * 0.5);
        }
    });

    return ViewPort;
});
