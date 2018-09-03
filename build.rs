//! Copied from https://github.com/sfackler/rust-phf example
//!

extern crate phf_codegen;

use std::env;
use std::fs::File;
use std::io::{BufWriter, Write};
use std::path::Path;

fn main() {
    let path = Path::new(&env::var("OUT_DIR").unwrap()).join("codegen.rs");
    let mut file = BufWriter::new(File::create(&path).unwrap());

    write!(
        &mut file,
        "static EMOJI_MAP: phf::Map<&'static str, &'static str> = "
    ).unwrap();
    let mut emoji_map = phf_codegen::Map::new();
    emoji_map.entry("extern", "another");
    emoji_map.build(&mut file).unwrap();
    write!(&mut file, ";\n").unwrap();
}
