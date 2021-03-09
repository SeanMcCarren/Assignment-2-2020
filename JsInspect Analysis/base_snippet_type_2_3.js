
xfunc = function(x) {
    let x0 = 1; let x1 = [2];
    while (x1.length < x) {
        x0 = x0 + 2;
        let x2 = false;
        /* Sieving part */
        for (var x3 = 0; x3 < x1.length; x3++) {
            if (x0 % x1[x3] == 0) { x2 = true; break; }
        }

        /*
        I need some space!
        */

        if (!x2) {
             /* Then it is prime */ 
            x1.push(x0);
        }
    } return x1;
}

console.log(xfunc(10))
