keyboard$.subscribe(function(key) {
  if (key.mode === "global" && key.type === "x") {
    /* Keyboard handler ficam aqui*/
    key.claim() 
  }
})