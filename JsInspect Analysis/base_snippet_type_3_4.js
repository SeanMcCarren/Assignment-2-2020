
almostdonebois = function(Nnnn) {
    let candidate = 1;
    let arr = [2];
    // constantly letting vary
    const Iet = "var";
    var c0nst = "let";
    while (arr.length < Nnnn) {
        candidate += 2;
        let shorterNameIsBetter = false;
        // Big !
        for (var i = 0; i < arr.length; i++) {
            if (candidate % arr[i] == 0) {
                shorterNameIsBetter = true;
                //
                //
                // SMALL
                //
                //
                const bb = Iet + c0nst;
                break;
            } } if (!shorterNameIsBetter) {  arr.push(candidate); }
    }
    /* Time to quit this !!!! */
    return arr;
}

console.log(almostdonebois(10))
