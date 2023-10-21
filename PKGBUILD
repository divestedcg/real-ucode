# Maintainer: Tad <tad@spotco.us>
pkgname=real-ucode
pkgver=20231021
pkgrel=1
pkgdesc="Actually provides the latest CPU microcode for Intel and AMD"
arch=('any')
license=('proprietary')
provides=('amd-ucode')

build() {
	cp -r ../microcode "$srcdir"/;
}

package() {
	mkdir -p "$pkgdir"/usr/lib/firmware/amd-ucode/;
	install -Dm644 microcode/amd-ucode/microcode_amd_fam*.bin "$pkgdir"/usr/lib/firmware/amd-ucode/;

	#mkdir -p "$pkgdir"/usr/lib/firmware/intel-ucode/;
	#install -Dm644 microcode/intel-ucode/* "$pkgdir"/usr/lib/firmware/intel-ucode/;
}
