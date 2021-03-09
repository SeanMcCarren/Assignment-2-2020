
primeSieve = function(x) {
    let c = 1; let a = [2];
    while (a.length < x) {
        c = c + 2;
        let helper = false;
        /* Sieving part */
        for (var i = 0; i < a.length; i++) {
            if (c % a[i] == 0) {
                helper = true; break;
            }
        }
        if (!helper) { /* Then it is prime */ a.push(c);}
    }
    return a;
}

console.log(primeSieve(10))
