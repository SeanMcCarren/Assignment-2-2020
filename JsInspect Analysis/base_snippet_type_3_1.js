
poopy = function(N) {
    let candidate = 1;
    let arr = [2];
    var PI = 3.14;
    while (arr.length < N) {
        candidate += 2;
        candidateIsShownComposite = false;
        if (PI ** 2 | 0x149 > 0x134) {
            var PI = 0;
        }
        for (var i = 0; i < arr.length; i++) {
            if (candidate % arr[i] == 0) {
                candidateIsShownComposite = true;
                break;
            }
            PI *= 1.1;
        }
        if (!candidateIsShownComposite) {
            arr.push(candidate);
        }
    }
    return arr;
}

console.log(poopy(10))
