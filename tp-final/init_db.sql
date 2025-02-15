CREATE DATABASE IF NOT EXISTS sentiment_db;
USE sentiment_db;

CREATE TABLE IF NOT EXISTS tweets (
    id INT AUTO_INCREMENT PRIMARY KEY,
    text TEXT NOT NULL,
    positive INT NOT NULL,
    negative INT NOT NULL
);

-- Insérer des tweets de test
INSERT INTO tweets (text, positive, negative) VALUES
-- 🔹 Tweets positifs
('J\'adore ce produit !', 1, 0),
('Super expérience, je recommande !', 1, 0),
('Ce film était incroyable !', 1, 0),
('Excellente qualité, très satisfait.', 1, 0),
('Je suis ravi de mon achat, merci !', 1, 0),
('Service client au top, je reviendrai.', 1, 0),
('Livraison rapide et produit conforme, parfait !', 1, 0),
('Une des meilleures expériences d\'achat en ligne.', 1, 0),
('Ce restaurant est exceptionnel, plats délicieux.', 1, 0),
('J\'ai adoré cet hôtel, service impeccable.', 1, 0),


-- 🔹 Tweets négatifs
('C\'est une catastrophe...', 0, 1),
('Décevant, je ne rachèterai pas.', 0, 1),
('Produit de mauvaise qualité, très déçu.', 0, 1),
('Service client inexistant, expérience horrible.', 0, 1),
('Livraison en retard et article endommagé.', 0, 1),
('Je déconseille fortement cet achat.', 0, 1),
('Mauvais rapport qualité-prix, à éviter.', 0, 1),
('Cet hôtel est une horreur, jamais vu ça.', 0, 1),
('Les plats étaient froids et immangeables.', 0, 1),
('Aucune assistance, une vraie arnaque.', 0, 1),
('Nul, vraiment pas bien.', 0, 1),

-- -- 🔹 Tweets neutres
-- ('Moyen, sans plus.', 0, 0),
-- ('Je suis mitigé sur ce restaurant.', 0, 0),
-- ('Bof, sans intérêt.', 0, 0),
-- ('Rien d\'exceptionnel, juste correct.', 0, 0),
-- ('L\'expérience était neutre, pas grand-chose à dire.', 0, 0),
-- ('Produit standard, ni bon ni mauvais.', 0, 0),
-- ('Service correct, mais sans plus.', 0, 0),
-- ('Un hôtel moyen, rien de spécial.', 0, 0),
-- ('Livraison dans les délais, sans problème particulier.', 0, 0),
-- ('Film passable, pas inoubliable.', 0, 0);
