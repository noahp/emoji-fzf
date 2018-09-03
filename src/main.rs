//! Command line utilty for listing emojis with keywords and printing emojis
//! from canonical name, for use with fzf-preview.

#[macro_use]
extern crate human_panic;
extern crate clap;
extern crate isatty;
extern crate phf;
use std::io;
use std::io::Read;

// static EMOJI_MAP: phf::Map<&'static str, &'static str>

fn main() {
    setup_panic!();

    // create the clap app
    let matches = clap::App::new(env!("CARGO_PKG_NAME"))
        .version(env!("CARGO_PKG_VERSION"))
        .author("Noah Pendleton / https://github.com/noahp")
        .about("CARGO_PKG_DESCRIPTION")
        .subcommand(clap::SubCommand::with_name("preview").about("List all emojis with keywords"))
        .subcommand(
            clap::SubCommand::with_name("get")
                .about("Print an emoji by canonical name")
                .arg(clap::Arg::with_name("NAME").help("canonical name")),
        ).get_matches();

    // execute subcommands
    match matches.subcommand_name() {
        Some("preview") => {
            println!("preview mode");
        }
        Some("get") => {
            println!("get mode");

            if !isatty::stdin_isatty() {
                let mut buffer = String::new();
                let mut reader = io::stdin();
                reader.read_to_string(&mut buffer).ok();
                print!("{}", buffer);
            }
        }
        _ => (),
    }
}
