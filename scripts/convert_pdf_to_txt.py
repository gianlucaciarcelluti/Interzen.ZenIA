#!/usr/bin/env python3
"""
Script per convertire file PDF a TXT usando pdfplumber.

Converte tutti i file PDF dalla cartella docs/fonti e salva i file TXT
in docs/fonti/txt_output/ mantenendo i nomi originali.

Uso:
    python3 scripts/convert_pdf_to_txt.py

Opzioni:
    --verbose    Mostra dettagli di conversione per ogni file
    --overwrite  Sovrascrivi file TXT esistenti
"""

import os
import sys
import argparse
import pdfplumber
import logging
from pathlib import Path
from datetime import datetime

# Configurazione logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class PDFtoTXTConverter:
    """Convertitore da PDF a TXT usando pdfplumber"""

    def __init__(self, verbose=False, overwrite=False):
        self.verbose = verbose
        self.overwrite = overwrite
        self.docs_root = Path(__file__).parent.parent / "docs"
        self.pdf_folder = self.docs_root / "fonti"
        self.output_folder = self.pdf_folder / "txt_output"
        self.stats = {
            'total': 0,
            'converted': 0,
            'skipped': 0,
            'failed': 0,
            'total_chars': 0
        }

    def setup_output_folder(self):
        """Crea la cartella di output se non esiste"""
        if not self.output_folder.exists():
            self.output_folder.mkdir(parents=True, exist_ok=True)
            logger.info(f"Creata cartella di output: {self.output_folder}")

        if not self.pdf_folder.exists():
            logger.error(f"Cartella fonti non trovata: {self.pdf_folder}")
            sys.exit(1)

    def get_pdf_files(self):
        """Trova tutti i file PDF nella cartella fonti"""
        pdf_files = list(self.pdf_folder.glob("*.pdf"))
        logger.info(f"Trovati {len(pdf_files)} file PDF in {self.pdf_folder}")
        return sorted(pdf_files)

    def convert_pdf(self, pdf_path):
        """Converte un singolo file PDF a TXT"""
        try:
            text_content = ""
            page_count = 0

            with pdfplumber.open(pdf_path) as pdf:
                page_count = len(pdf.pages)

                for page_num, page in enumerate(pdf.pages, 1):
                    try:
                        page_text = page.extract_text()
                        if page_text:
                            # Aggiungi numero di pagina
                            text_content += f"--- Pagina {page_num} ---\n"
                            text_content += page_text
                            text_content += "\n\n"
                    except Exception as e:
                        logger.warning(f"  Errore estrazione pagina {page_num}: {str(e)}")
                        continue

            if not text_content.strip():
                logger.warning(f"  ⚠️  File vuoto o nessun testo estratto: {pdf_path.name}")
                return None

            return {
                'content': text_content.strip(),
                'page_count': page_count,
                'char_count': len(text_content)
            }

        except Exception as e:
            logger.error(f"  ❌ Errore durante conversione: {str(e)}")
            return None

    def save_txt(self, pdf_path, conversion_result):
        """Salva il testo convertito in un file TXT"""
        try:
            # Crea nome file di output
            txt_filename = pdf_path.stem + ".txt"
            txt_path = self.output_folder / txt_filename

            # Controlla se il file esiste già
            if txt_path.exists() and not self.overwrite:
                logger.info(f"⏭️  SKIP: {txt_filename} (già esiste, usa --overwrite per sovrascrivere)")
                self.stats['skipped'] += 1
                return False

            # Salva il file
            with open(txt_path, 'w', encoding='utf-8') as f:
                f.write(conversion_result['content'])

            char_count = conversion_result['char_count']
            page_count = conversion_result['page_count']
            self.stats['total_chars'] += char_count

            if self.verbose:
                logger.info(f"✅ CONVERTED: {txt_filename} ({page_count} pagine, {char_count} caratteri)")
            else:
                logger.info(f"✅ CONVERTED: {txt_filename}")

            self.stats['converted'] += 1
            return True

        except Exception as e:
            logger.error(f"  ❌ Errore nel salvataggio: {str(e)}")
            return False

    def process_all(self):
        """Processa tutti i file PDF nella cartella"""
        self.setup_output_folder()
        pdf_files = self.get_pdf_files()

        if not pdf_files:
            logger.warning("Nessun file PDF trovato!")
            return

        logger.info(f"\n{'='*70}")
        logger.info(f"Inizio conversione PDF → TXT")
        logger.info(f"{'='*70}\n")

        for pdf_path in pdf_files:
            self.stats['total'] += 1
            logger.info(f"\n[{self.stats['total']}/{len(pdf_files)}] {pdf_path.name}")

            # Converti PDF
            result = self.convert_pdf(pdf_path)

            if result:
                # Salva TXT
                self.save_txt(pdf_path, result)
            else:
                logger.warning(f"⏭️  SKIP: Conversione fallita")
                self.stats['failed'] += 1

        # Stampa statistiche
        self.print_summary()

    def print_summary(self):
        """Stampa il riepilogo della conversione"""
        logger.info(f"\n{'='*70}")
        logger.info(f"RIEPILOGO CONVERSIONE")
        logger.info(f"{'='*70}")
        logger.info(f"Total files:      {self.stats['total']}")
        logger.info(f"Converted:        {self.stats['converted']} ✅")
        logger.info(f"Skipped:          {self.stats['skipped']} ⏭️")
        logger.info(f"Failed:           {self.stats['failed']} ❌")
        logger.info(f"Total characters: {self.stats['total_chars']:,}")
        logger.info(f"Output folder:    {self.output_folder}")
        logger.info(f"{'='*70}\n")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Converti file PDF da docs/fonti a TXT in docs/fonti/txt_output',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Esempi:
  python3 scripts/convert_pdf_to_txt.py                # Conversione standard
  python3 scripts/convert_pdf_to_txt.py --verbose      # Con dettagli
  python3 scripts/convert_pdf_to_txt.py --overwrite    # Sovrascrivi TXT esistenti
  python3 scripts/convert_pdf_to_txt.py -v -o          # Entrambi i flag
        '''
    )

    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Mostra dettagli di conversione per ogni file'
    )

    parser.add_argument(
        '-o', '--overwrite',
        action='store_true',
        help='Sovrascrivi file TXT esistenti'
    )

    args = parser.parse_args()

    # Crea convertitore e processa
    converter = PDFtoTXTConverter(verbose=args.verbose, overwrite=args.overwrite)
    converter.process_all()


if __name__ == '__main__':
    main()
