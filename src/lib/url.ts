/**
 * Construit une URL interne en tenant compte du chemin de base.
 *
 * Le site peut etre servi a la racine d'un domaine (azur-grill-epinay.fr)
 * ou sous un sous-chemin (github.io/azur-grill/). Un `href="/carte"` ecrit
 * en dur fonctionne dans le premier cas et pointe hors du site dans le
 * second — d'ou ce passage oblige par BASE_URL, qu'Astro renseigne selon
 * la configuration de build.
 */
export function lien(chemin: string): string {
  const base = import.meta.env.BASE_URL.replace(/\/+$/, '');
  const suite = chemin.replace(/^\/+/, '');
  return suite ? `${base}/${suite}` : `${base}/`;
}
