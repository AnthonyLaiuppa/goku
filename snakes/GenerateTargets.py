from __future__ import absolute_import, unicode_literals
import sublist3r


class GenerateTargets(object):
	
	def __init__(self, domain=None, names={}):
		self.domain=domain
		self.names=names

	def get_subs(self):
		output = self.domain.replace('https://', '') + '_subdomains.txt'
		subdomains = sublist3r.main(
			self.domain.replace('https://', ''),
			40,
			output,
			ports=None,
			silent=False,
			verbose=False,
			enable_bruteforce=False,
			engines=None
		)
		self.subdomains = subdomains
		self.subdomains.append(self.domain)
		for sub in self.subdomains:
			name = sub
			name = name.replace('https://', '').replace('.com', ' ')
			name = name.strip()
			self.names[name] = sub

	def generate_scripts(self):

		commands = []

		for k,v in self.names.items():
			og = open("pod.yml")
			copy_name = k.replace('.','-') + '.yml'
			copy = open(copy_name, "w+")
			command = 'kubectl apply -f {0}\n'.format(copy_name)
			commands.append(command)
			for line in og:

				if '{{pod_name}}' in line:
					line = line.replace("{{pod_name}}", k.replace('.','-'))
					copy.write(line)

				elif '{{url}}' in line:
					if 'https://' not in v:
						v = 'https://' + v
					line = line.replace("{{url}}", v) 
					copy.write(line)

				else:
					copy.write(line)

			og.close()
			copy.close()

			ms = open("mass_scan.sh", "w+")
			for command in commands:
				ms.write(command)
			ms.close()

if __name__ == "__main__":
	domain = "https://example_placeholder.com"
	goku = GenerateTargets(domain)
	goku.get_subs()
	goku.generate_scripts()
