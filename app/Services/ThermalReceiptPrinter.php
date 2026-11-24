<?php

namespace App\Services;

use Carbon\Carbon;
use Illuminate\Support\Facades\Log;
use Symfony\Component\Process\Process;

class ThermalReceiptPrinter
{
    /**
     * @param  array{
     *     heading?: string,
     *     student_name?: string,
     *     id_number?: string,
     *     served_by?: string,
     *     books?: list<array{title?: string, author?: string, barcode?: string, due_date?: string, extra?: list<string>}>
     * }  $receipt
     */
    public function print(array $receipt): bool
    {
        if (app()->runningUnitTests()) {
            return true;
        }

        $printer = trim((string) config('printing.thermal_printer', 'GLPrint'));
        if ($printer === '' || PHP_OS_FAMILY !== 'Windows') {
            Log::warning('Thermal receipt was not printed.', ['printer' => $printer]);

            return false;
        }

        $file = tempnam(sys_get_temp_dir(), 'pbcc-receipt-');
        if ($file === false) {
            return false;
        }

        try {
            file_put_contents($file, $this->bytes($receipt));

            $powershell = getenv('SystemRoot')
                ? getenv('SystemRoot').'\\System32\\WindowsPowerShell\\v1.0\\powershell.exe'
                : 'powershell.exe';

            $process = new Process([
                $powershell,
                '-NoProfile',
                '-NonInteractive',
                '-ExecutionPolicy',
                'Bypass',
                '-File',
                base_path('scripts/raw-print.ps1'),
                '-PrinterName',
                $printer,
                '-FilePath',
                $file,
            ]);
            $process->setTimeout(20);
            $process->run();

            if (! $process->isSuccessful()) {
                Log::warning('Thermal receipt print failed.', [
                    'printer' => $printer,
                    'exit' => $process->getExitCode(),
                    'error' => trim($process->getErrorOutput().$process->getOutput()),
                ]);

                return false;
            }

            return true;
        } catch (\Throwable $e) {
            Log::warning('Thermal receipt print failed.', [
                'printer' => $printer,
                'error' => $e->getMessage(),
            ]);

            return false;
        } finally {
            @unlink($file);
        }
    }

    /**
     * @param  array{
     *     heading?: string,
     *     student_name?: string,
     *     id_number?: string,
     *     served_by?: string,
     *     books?: list<array{title?: string, author?: string, barcode?: string, due_date?: string, extra?: list<string>}>
     * }  $receipt
     */
    public function bytes(array $receipt): string
    {
        $when = Carbon::now('Asia/Manila')->format('n/j/Y g:i:s A');
        $servedBy = trim((string) ($receipt['served_by'] ?? ''));
        $servedLine = $servedBy !== '' ? $servedBy : '______________________';

        $lines = [];
        foreach ($this->wrap((string) config('printing.library_name'), 32) as $line) {
            $lines[] = $line;
        }
        $lines[] = $when;
        $lines[] = '';
        $lines[] = '';
        $lines[] = strtoupper(trim((string) ($receipt['student_name'] ?? '')));
        $lines[] = (string) ($receipt['id_number'] ?? '');
        $lines[] = '';
        $lines[] = (string) ($receipt['heading'] ?? "Today's Checkouts");
        $lines[] = '--------------------------------';

        foreach ($receipt['books'] ?? [] as $book) {
            $lines[] = (string) ($book['title'] ?? '');
            $lines[] = (string) ($book['author'] ?? '');
            $lines[] = 'Barcode: '.((string) ($book['barcode'] ?? ''));
            $lines[] = 'Due Date: '.((string) ($book['due_date'] ?? ''));
            foreach ($book['extra'] ?? [] as $extra) {
                $lines[] = (string) $extra;
            }
            $lines[] = '--------------------------------';
        }

        $lines[] = 'Served By: '.$servedLine;
        $lines[] = '';
        $lines[] = '';
        $lines[] = '';

        $text = implode("\n", $lines)."\n";
        $encoded = iconv('UTF-8', 'Windows-1252//TRANSLIT//IGNORE', $text);
        if ($encoded === false) {
            $encoded = $text;
        }

        return "\x1B\x40\x1B\x61\x00".$encoded."\x1D\x56\x01";
    }

    /**
     * @return list<string>
     */
    protected function wrap(string $text, int $width): array
    {
        $text = trim(preg_replace('/\s+/', ' ', $text) ?? '');
        if ($text === '') {
            return [];
        }

        return explode("\n", wordwrap($text, $width, "\n", true));
    }
}
