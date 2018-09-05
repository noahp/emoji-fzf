//! Copied from https://github.com/sfackler/rust-phf example
//!

extern crate phf_codegen;
extern crate serde_json;
#[macro_use]
extern crate serde_derive;

use std::env;
use std::fs::File;
use std::io::{BufWriter, Write};
use std::path::Path;
use std::collections::HashMap;

#[derive(Deserialize, Debug)]
struct EmojiEntry {
    keywords: Vec<String>,
    char: String,
}

fn main() {
    let path = Path::new(&env::var("OUT_DIR").unwrap()).join("codegen.rs");
    let mut file = BufWriter::new(File::create(&path).unwrap());

    write!(
        &mut file,
        "static EMOJI_MAP: phf::Map<&'static str, &'static str> = "
    ).unwrap();
    let mut emoji_phf: phf_codegen::Map<String> = phf_codegen::Map::new();

    let emoji_raw = r#"{
        "grinning": {
            "keywords": ["face", "smile", "happy", "joy", ":D", "grin"],
            "char": "😀",
            "fitzpatrick_scale": false,
            "category": "people"
        },
        "grimacing": {
            "keywords": ["face", "grimace", "teeth"],
            "char": "😬",
            "fitzpatrick_scale": false,
            "category": "people"
        }
    }"#;

    let emoji_map: HashMap<String, EmojiEntry> = serde_json::from_str(emoji_raw).unwrap();

    println!("{:#?}", emoji_map);

    // for (key, value) in emoji_map {
    //     emoji_map.entry(key, value);
    // }

    emoji_phf.build(&mut file).unwrap();
    write!(&mut file, ";\n").unwrap();
}
