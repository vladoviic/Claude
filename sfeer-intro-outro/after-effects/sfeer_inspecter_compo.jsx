// SFEER · Inspecter la compo active
// Lit la compo ouverte (et toutes ses précompos) sans rien modifier, et écrit un rapport texte
// sur le Bureau : sfeer_inspection_<compo>.txt. Envoie ce fichier à Claude.
// Fichier > Scripts > Exécuter le fichier de script…  (Préférences > Scripts et expressions >
// « Autoriser les scripts à écrire des fichiers et à accéder au réseau » doit être coché).
(function () {
    var comp = app.project.activeItem;
    if (!(comp instanceof CompItem)) { alert("Ouvre d'abord la compo à inspecter (clic dans le Montage)."); return; }
    var out = [], seen = {}, MAXK = 400;

    function r(v) { return Math.round(v * 100) / 100; }
    function val(v) {
        if (v === null || v === undefined) { return "null"; }
        if (v instanceof Array) { var a = []; for (var i = 0; i < v.length; i++) { a.push(val(v[i])); } return "[" + a.join(",") + "]"; }
        if (typeof v === "number") { return String(r(v)); }
        if (typeof v === "boolean" || typeof v === "string") { return String(v); }
        try {
            if (v.vertices !== undefined) {            // Shape
                var s = "Shape(" + v.vertices.length + " sommets, fermé=" + v.closed + " : ";
                var pts = [];
                for (var k = 0; k < v.vertices.length; k++) {
                    pts.push(val(v.vertices[k]) + "/" + val(v.inTangents[k]) + "/" + val(v.outTangents[k]));
                }
                return s + pts.join(" ") + ")";
            }
            if (v.text !== undefined) { return "Texte(\"" + v.text + "\", " + v.font + ", " + v.fontSize + ")"; }
        } catch (e) {}
        return String(v);
    }
    function pad(n) { var s = ""; for (var i = 0; i < n; i++) { s += "  "; } return s; }

    function dumpProp(p, depth) {
        if (p.propertyType === PropertyType.PROPERTY) {
            var hasK = p.numKeys > 0, hasE = false;
            try { hasE = p.expressionEnabled && p.expression !== ""; } catch (e) {}
            var modified = true;
            try { modified = p.isModified; } catch (e2) {}
            if (!hasK && !hasE && !modified) { return; }
            if (p.propertyValueType === PropertyValueType.NO_VALUE) { return; }
            var line = pad(depth) + "· " + p.name + " [" + p.matchName + "]";
            if (!hasK) {
                try { line += " = " + val(p.value); } catch (e3) {}
            }
            out.push(line);
            if (hasK) {
                for (var k = 1; k <= Math.min(p.numKeys, MAXK); k++) {
                    var ki = "";
                    try {
                        var ie = p.keyInTemporalEase(k), oe = p.keyOutTemporalEase(k);
                        ki = " in(" + r(ie[0].speed) + "," + r(ie[0].influence) + "%) out(" + r(oe[0].speed) + "," + r(oe[0].influence) + "%)";
                        ki += " interp " + p.keyInInterpolationType(k) + "/" + p.keyOutInterpolationType(k);
                    } catch (e4) {}
                    out.push(pad(depth + 1) + "clé " + k + " t=" + r(p.keyTime(k)) + "s (" + Math.round(p.keyTime(k) * comp.frameRate) + "i) = " + val(p.keyValue(k)) + ki);
                }
                if (p.numKeys > MAXK) { out.push(pad(depth + 1) + "… " + (p.numKeys - MAXK) + " clés de plus"); }
            }
            if (hasE) { out.push(pad(depth + 1) + "expression : " + p.expression.replace(/\r?\n/g, " ⏎ ")); }
        } else {
            var head = pad(depth) + "▸ " + p.name + " [" + p.matchName + "]";
            try { if (p.enabled === false) { head += " (désactivé)"; } } catch (e5) {}
            var before = out.length;
            out.push(head);
            for (var i = 1; i <= p.numProperties; i++) { dumpProp(p.property(i), depth + 1); }
            if (out.length === before + 1 && depth > 1) { out.pop(); }   // groupe vide : on n'encombre pas
        }
    }

    function dumpComp(c, depth) {
        if (seen[c.id]) { out.push(pad(depth) + "(précompo « " + c.name + " » déjà décrite plus haut)"); return; }
        seen[c.id] = true;
        out.push("");
        out.push(pad(depth) + "══ COMPO « " + c.name + " » " + c.width + "x" + c.height + ", " + r(c.duration) + " s, " + c.frameRate + " i/s, " + c.numLayers + " calques");
        var mk = c.markerProperty;
        for (var m = 1; m <= mk.numKeys; m++) {
            out.push(pad(depth) + "  repère t=" + r(mk.keyTime(m)) + "s : " + mk.keyValue(m).comment);
        }
        var pre = [];
        for (var i = 1; i <= c.numLayers; i++) {
            var L = c.layer(i);
            var kind = "AV";
            if (L instanceof TextLayer) { kind = "texte"; }
            else if (L instanceof ShapeLayer) { kind = "forme"; }
            else if (L instanceof CameraLayer) { kind = "caméra"; }
            else if (L instanceof LightLayer) { kind = "lumière"; }
            else if (L.nullLayer) { kind = "nul"; }
            else if (L.adjustmentLayer) { kind = "réglage"; }
            else if (L.source instanceof CompItem) { kind = "précompo « " + L.source.name + " »"; pre.push(L.source); }
            else if (L.source && L.source.mainSource instanceof SolidSource) { kind = "solide " + val(L.source.mainSource.color); }
            else if (L.source) { kind = "métrage « " + L.source.name + " »"; }
            var info = "#" + i + " « " + L.name + " » — " + kind + " — " + r(L.inPoint) + "→" + r(L.outPoint) + "s";
            if (!L.enabled) { info += " — masqué"; }
            try { if (L.guideLayer) { info += " — GUIDE"; } } catch (e) {}
            try { if (L.parent) { info += " — parent #" + L.parent.index; } } catch (e1) {}
            try { if (L.hasTrackMatte) { info += " — cache " + L.trackMatteType + (L.trackMatteLayer ? " par #" + L.trackMatteLayer.index : ""); } } catch (e2) {}
            try { if (L.isTrackMatte) { info += " — sert de cache"; } } catch (e3) {}
            try { info += " — mode " + L.blendingMode + (L.motionBlur ? " — flou de bougé" : "") + (L.collapseTransformation ? " — rastérisation continue" : ""); } catch (e4) {}
            out.push("");
            out.push(pad(depth) + info);
            for (var p = 1; p <= L.numProperties; p++) { dumpProp(L.property(p), depth + 1); }
        }
        for (var q = 0; q < pre.length; q++) { dumpComp(pre[q], depth + 1); }
    }

    out.push("SFEER · inspection de « " + comp.name + " » — " + app.project.file + " — AE " + app.version);
    dumpComp(comp, 0);
    var f = new File(Folder.desktop.fsName + "/sfeer_inspection_" + comp.name.replace(/[^A-Za-z0-9_-]+/g, "_") + ".txt");
    f.encoding = "UTF-8";
    if (!f.open("w")) { alert("Impossible d'écrire sur le Bureau. Coche Préférences > Scripts et expressions > Autoriser les scripts à écrire des fichiers."); return; }
    f.write(out.join("\n"));
    f.close();
    alert("Rapport écrit sur le Bureau :\n" + f.fsName + "\n\nEnvoie ce fichier à Claude.");
})();
