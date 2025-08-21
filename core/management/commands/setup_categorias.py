from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Category


class Command(BaseCommand):
    help = 'Cria categorias públicas padrão para o sistema'

    def handle(self, *args, **options):
        # Criar superusuário admin se não existir
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@sistema.com',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            self.stdout.write(
                self.style.SUCCESS('Superusuário "admin" criado com senha "admin123"')
            )
        
        # Categorias públicas padrão
        categorias_publicas = [
            ('Alimentação', 'Gastos com comida, restaurantes, supermercado'),
            ('Transporte', 'Combustível, transporte público, Uber, manutenção veicular'),
            ('Moradia', 'Aluguel, condomínio, IPTU, financiamento'),
            ('Saúde', 'Medicamentos, consultas, planos de saúde'),
            ('Educação', 'Cursos, livros, material escolar'),
            ('Lazer', 'Cinema, viagens, entretenimento'),
            ('Vestuário', 'Roupas, calçados, acessórios'),
            ('Tecnologia', 'Eletrônicos, software, internet'),
            ('Serviços', 'Limpeza, manutenção, profissionais autônomos'),
            ('Outros', 'Despesas diversas não categorizadas'),
        ]
        
        categorias_criadas = 0
        for nome, descricao in categorias_publicas:
            categoria, created = Category.objects.get_or_create(
                name=nome,
                user=admin_user,
                defaults={
                    'description': descricao,
                    'is_public': True,
                }
            )
            
            if created:
                categorias_criadas += 1
                self.stdout.write(f'✓ Categoria "{nome}" criada')
            else:
                # Se já existe, garantir que seja pública
                categoria.is_public = True
                categoria.save()
                self.stdout.write(f'→ Categoria "{nome}" já existia')
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\n{categorias_criadas} categorias públicas criadas/atualizadas com sucesso!'
            )
        )
        
        self.stdout.write(
            self.style.WARNING(
                '\nDica: Faça login como admin (admin/admin123) para gerenciar categorias públicas'
            )
        )
