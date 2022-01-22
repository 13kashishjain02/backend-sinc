from rest_framework import routers, serializers, viewsets

from account.models import Account,InvestorAccount,Startup


class RegistrationSerializer(serializers.ModelSerializer):

	password2 				= serializers.CharField(style={'input_type': 'password'}, write_only=True)

	class Meta:
		model = Account
		fields = ('email', 'name', 'contact_number', 'password', 'password2')
		extra_kwargs = {
				'password': {'write_only': True},
		}


	def	save(self):

		account = Account(
					email=self.validated_data['email'],
					name=self.validated_data['name'],
                    contact_number = self.validated_data['contact_number'],
				)
		password = self.validated_data['password']
		password2 = self.validated_data['password2']
		if password != password2:
			raise serializers.ValidationError({'password': 'Passwords must match.'})
		account.set_password(password)
		account.save()
		return account


class InvestorSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvestorAccount
        fields = ('__all__')

class StartupSerializer(serializers.ModelSerializer):
    class Meta:
        model=Startup
        fields=('__all__')