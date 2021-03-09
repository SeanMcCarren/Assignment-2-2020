
getPrimes = function(n) {
    let c = 1;
    let a = [2];
    while (a.length < n) {
        c = c + 2;
        let candidateIsShownComposite = false;
        for (var i = 0; i < a.length; i++) {
            if (c % a[i] == 0) {
                candidateIsShownComposite = true;
                break;
            }
        }
        if (!candidateIsShownComposite) {
            a.push(c);
        }
    }
    return a;
}

console.log(getPrimes(10))
