
snoopy = function(Nxxx) {
    let candidate = 1;
    let arr = [2]; var PI = 3.14;
    while (arr.length < Nxxx) {
        candidate += 2; let candidateIsShownComposite = false;
        for (var i = 0; i < arr.length; i++) {
            if (candidate % arr[i] == 0) {
                candidateIsShownComposite = true;
                break;
            }
            PI *= 1.1;
        }
        if (!candidateIsShownComposite) {
            arr.push(candidate);
// Hi
        }
    }
    return arr;
}

console.log(snoopy(10))
